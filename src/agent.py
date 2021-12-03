from recipe import Recipe
from aenum import Enum, unique, auto, extend_enum
from transformers import pipeline
import spacy
import pandas as pd
import numpy as np

# A class determining possible intents for our agent
class Intent(Enum):
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

		# Associating the enum with a function inside of Agent class
		self.f = lambda: None


# Our agent
class Agent():

	def __init__(self):

		# General bot information
		self.name = 'This is the bot\'s name!'
		self.recipe = None
		self.classifier = pipeline('zero-shot-classification')

		# Associating intents with agent functions
		self.intents = Intent
		for intent in self.intents:
			self.associate(intent)

		# Our initial state
		self.current = None
		self.current_intent = self.intents.UNKNOWN

	# Associates intents with agent functions
	@classmethod
	def associate(cls, intent):
		intent.f = getattr(cls, intent.value, lambda: None)

	# Given a string of natural language, returns an intent
	def parse_intent(self, text):
		pass

	# When the user's intent is to display broad information about the recipe
	def show(self, text):
		pass

	# When the user's intent is to navigate to a different step of the recipe
	def navigate(self, text):
		pass

	# When the user's intent is to find information online
	def search(self, text):
		pass

	# When the user's intent is to get some parameter about an ingredient or step
	def get_param(self, text):
		pass

	# When the user's intent is not understood
	def unknown(self, text):
		print(f'Sorry, we didn\'t quite understand that. Could you try again?')

	# When the user's intent is to find a suitable substitute for an ingredient
	def substitute(self, text):
		pass

	# Call to run the bot
	def run(self):
		
		print(f'Hello, and welcome to Nathan\'s cooking assistant. My name is {self.name}, and I will guide you through any recipe from AllRecipes.com! Please input a recipe URL to get started.')

		url = input('Your recipe URL: ')
		self.recipe = Recipe(url)

		while self.current_intent is not self.intents.QUIT:
			user_input = input('Your Response: ')
			self.current_intent = self.parse_intent(user_input)
			self.current_intent.f(user_input)

		print('Glad I could be of assistance!')

		

def main():

	# Loading spacy
	nlp = spacy.load("en_core_web_sm")

	# Loading up the conversational agent
	agent = Agent()
	agent.run()


if __name__ == '__main__':
	main()