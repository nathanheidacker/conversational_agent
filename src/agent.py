from recipe import Recipe
from aenum import Enum, unique, auto, extend_enum
from transformers import pipeline
import wordninja
import spacy
import re
import pandas as pd
import numpy as np
import requests
import bs4
import nltk
import data

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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

		# Checking explicitly for URLs
		if 'www.allrecipes.com/recipe/' in text:
			return self.intents.START

		if len(text.split()) > 0 and text.split()[0] in [intent.value for intent in self.intents]:
			return self.intents(text.split()[0])

		elif re.match(r'^[qQ]([uU]?[iI]?[tT]?)$', text):
			return self.intents.QUIT

		return self.intents.UNKNOWN

	# When the user's intent is to start a new recipe
	def start(self, text=None):

		# Begin by parsing the input text for a recipe
		url = re.search(r'.*(https://www\.allrecipes\.com/recipe/[0-9]+/.+/)', text)
		url = url.group(1) if url else ''

		# Skip asking the user the first time if we find a url
		skip_first = True if url else False

		# Allows the user to start on another recipe immediately
		self.recipe = None

		# Continue until we find a recipe or quit explicitly
		while self.recipe is None and not re.match(r'^[qQ]([uU]?[iI]?[tT]?)$', url):

			# We want to skip the first url request if the url has been provided in the query text
			if not skip_first:
				print('Please provide a recipe url from AllRecipes.com')
				url = input('URL: ')
			skip_first = False

			try:
				self.recipe = Recipe(url)
				self.current = self.recipe.steps[0]
				self.current_i = 0

				# Successful parse
				print(f'Okay. Today I\'ll be helping you make {self.recipe.recipe_name}. What\'s next?')

			except ValueError:
				print('Sorry, we couldn\'t parse that url. Please try another, or type q to quit\n')


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

		print(self.current)

	# When the user's intent is to find information online
	def search(self, text):

		# Getting the inquiry from the text
		inquiry = ' '.join(text.split()[1:]).replace('?', '')

		do_can_words = ["can", "could",  "do", "carry out", "execute", "perform", "implement", "complete", "finish", "bring about", "effect", "pull off"]
		assumes_vague = ["this", "that", "these", "those", "such"]

		# Adding words to make the google query more accurate
		for q_word in ['what is', 'what\'s', 'whats']:
			if q_word in inquiry.lower():

				tools = self.recipe.tools if self.recipe else data.tools
				for tool in tools:
					if tool in inquiry:
						inquiry += 'tool'
						break

				# Helps with query accuracy
				if 'for cooking' not in inquiry.lower():
					inquiry += ' for cooking'

        # Finding out if the question is a vague one
		step = nltk.word_tokenize(inquiry)
		vague_question = False

		for vague_word in assumes_vague:
			if vague_word in inquiry:
				vague_question = True
				break

		tags = ' '.join([tag for _, tag in nltk.pos_tag(step)])
		vague_question = False if 'NN' in tags else vague_question

		# Vague questions are not permitted unless we have an active recipe
		if not self.recipe and vague_question:
			print('It seems that you\'re asking a question about a recipe, but you aren\'t current in one.')
			return

        # Making the inquiry more explicit if it is vague
		inquiry = ("How do I " + inquiry) if vague_question else inquiry
			
		# Getting the google result
		url = "https://google.com/search?q=" + inquiry
		request_result = requests.get(url)
		soup = bs4.BeautifulSoup(request_result.text, 'html.parser')
		answer = soup.find("div", class_='BNeawe s3v9rd AP7Wnd').text
		answer = answer.replace('... ', ' ').replace('  ', ' ')
		print(answer)

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
				action(user_input)
				print()
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
