from recipe import Recipe
from aenum import Enum, unique, auto, extend_enum
from transformers import pipeline
import spacy
import re
import pandas as pd
import numpy as np

# A class determining possible intents for our agent
class Intent(Enum):
	START = 'start'
	SHOW = 'show'
	NAVIGATE = 'navigate'
	SEARCH = 'search'
	GET_PARAM = 'get_param'
	SUBSTITUTE = 'substitute'
	QUIT = 'quit'
	UNKNOWN = 'unknown'


	def __init__(self, value, index=[0]):

		# Giving the enum an index for category determination
		self.i = index[0]
		index[0] += 1


# Our conversational agent
class Agent():

	def __init__(self):

		# General bot information
		self.name = 'RecipeBot'
		self.recipe = None
		#self.classifier = pipeline('zero-shot-classification')

		# Associating intents with agent functions
		self.intents = Intent

		# Our initial state
		self.current = None
		self.current_i = None
		self.current_intent = self.intents.UNKNOWN

		# Keeping a history of actions
		self.history = []

	# Get the corresponding function for an intent
	def intent_action(self, intent=None):
		if intent is None:
			intent = self.current_intent
		return getattr(self, intent.value, lambda *args: None)

	# Given a string of natural language, returns an intent
	def parse_intent(self, text):
		if text in [intent.value for intent in self.intents]:
			return self.intents(text)

		elif re.match(r'^[qQ]([uU]?[iI]?[tT]?)$', text):
			return self.intents.QUIT

		return self.intents.UNKNOWN

	# When the user's intent is to start a new recipe
	def start(self, text=None):
		print('Please provide a recipe url from AllRecipes.com')

		url = ''

		while self.recipe is None and not re.match(r'^[qQ]([uU]?[iI]?[tT]?)$', url):

			url = input('URL: ')

			try:
				self.recipe = Recipe(url)
				self.current = self.recipe.steps[0]
				self.current_i = 0

				# Successful parse
				print(f'Okay. Today I\'ll be helping you make {self.recipe.recipe_name}.')

			except ValueError:
				print('Sorry, we couldn\'t parse that url. Please try another, or type q to quit')


	# When the user's intent is to display broad information about the recipe
	def show(self, text):
		print(self.current.text)

	# When the user's intent is to navigate to a different step of the recipe
	def navigate(self, text):

		# determine where/how to move
		# SOME FUNCTION HERE
		direction = 'forward'

		# Moving
		if direction == 'forward':
			self.current_i += 1
		else:
			self.current_i -= 1

		self.current = self.recipe.steps[self.current_i]

	# When the user's intent is to find information online
	def search(self, text):
		pass

	# When the user's intent is to get some parameter about an ingredient or step
	def get_param(self, text):
		pass

	# When the user's intent is to find a suitable substitute for an ingredient
	def substitute(self, text):
		pass

	# When the user's intent is not understood
	def unknown(self, text):
		print(f'Sorry, I didn\'t quite understand that. Could you try again?')

	# Call to run the bot
	def run(self):

		# Intents that require us to be working with a recipe.
		require_recipe = [Intent.SHOW, self.intents.NAVIGATE, self.intents.GET_PARAM]
		
		print(f'\nHello, and welcome to Nathan, Jason, and Ricky\'s cooking assistant. My name is {self.name}, and I will guide you through any recipe from AllRecipes.com! How can I be of service today?')

		ask = True

		while self.current_intent is not self.intents.QUIT:

			# The user input
			if ask:
				user_input = input('Your Query: ')

			self.current_intent = self.parse_intent(user_input)
			ask = True

			# In the case that the user is not currently in a recipe, but is trying to perform an action that requires one
			if self.current is None and self.current_intent in require_recipe:
				
				print(f'\nSorry, but it seems like you\'re trying to do something that requires a specific recipe. Would you like to start on one now?')

				user_input = input('Start recipe? (y/n): ')
				
				if user_input.lower() == 'y':
					self.start()

				elif user_input.lower() == 'n':
					print('\nOk. Let me know if you need anything else')

				else:
					ask = False

			# The user is currently in a recipe (all actions available)
			else:
				action = self.intent_action()
				print()
				action(user_input)
				self.history.append((self.current_intent.name, user_input))

		print('Glad I could be of assistance!')

		

def main():

	# Loading spacy
	nlp = spacy.load("en_core_web_sm")

	# Loading up the conversational agent
	agent = Agent()
	agent.run()

	# DEBUGGING
	print('\n\n--ACTION HISTORY--\n')
	for action in agent.history: print(action)


if __name__ == '__main__':
	main()