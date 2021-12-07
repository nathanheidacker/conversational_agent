from bs4 import BeautifulSoup as bs
from urllib import request
from functools import lru_cache
from transformers import pipeline
import data
import requests
import unicodedata
import re
import spacy

# Loading spacy
nlp = spacy.load("en_core_web_sm")


# Class representing a recipe
class Recipe:

	# Class representing a node in a step graph
	class Step:

		def __init__(self, sentence=None):

			# Null/empty step
			if sentence is None:
				self.text = ''
				self.actions, self.ingredients, self.tools = [], [], []
				self.new_text = ''
				self.time = None

			# Parsing step
			else:
				self.text = ' '.join([self.convert_fraction(x) for x in sentence.split()])
				self.tokens = nlp(sentence)
				self.actions, self.ingredients, self.tools, self.valid = self.get_info()
				self.new_text = ' '.join([self.convert_fraction(x) for x in sentence.split()])
				self.time = self.get_time()
				self.temp = self.get_temp()
				self.quantities = self.get_quantities()

		def __str__(self):
			return f'(Actions: {self.actions} | Ingredients: {self.ingredients} | Tools: {self.tools} | Time: {self.time})'

		def __repr__(self):
			return str(self)

		# Filling step info
		def get_info(self):

			# Getting items from data, then querying for missing items
			actions, ingredients, tools = self.from_data()

			# QUERYING ITEMS IN THE TEXT
			#actions, ingredients, tools = self.query(actions, ingredients, tools)

			valid = True if (actions and (ingredients or tools)) else False

			return actions, ingredients, tools, valid

		# Grabbing potential data from hardcoded lists
		def from_data(self):
			# Getting actions
			actions = [w.text for w in self.tokens if w.lemma_ in data.cooking_methods]

			# Getting ingredients
			ingredients = [w.text for w in self.tokens if w.lemma_ in data.all_ingredients]

			# Getting tools
			tools = [w.text for w in self.tokens if w.lemma_ in data.tools]

			return actions, ingredients, tools

		# Finding more data with queries
		def query(self, actions, ingredients, tools):

			# Given a question as a string, returns an answer and a confidence in that answer
			def answer(question):
				qdict = {
					'question': question,
					'context': self.text
				}

				return query(qdict)['answer'], query(qdict)['score']

			def append_answer(l, question, threshold=0):
				item, confidence = answer(question)
				if confidence > threshold and len(item.split()) < 4:
					l.append((item, confidence))

			# Querying actions
			if not actions:

				# Querying using ingredients
				for ingredient in ingredients:
					question = f'do what with {ingredient}?'
					append_answer(actions, question)

				# Querying using tools
				for tool in tools:
					question = f'do what with {tool}?'
					append_answer(actions, question)

			# Deleting duplicates
			actions = list(set(actions))

			# Querying ingredients
			if not ingredients:

				for action in actions:
					question = f'{action} what?'
					append_answer(ingredients, question)

			ingredients = list(set(ingredients))

			# Querying tools
			if not tools:

				for action in actions:
					for ingredient in ingredients:
						question = f'{action} {ingredient} in a what?'
						append_answer(tools, question)

			tools = list(set(tools))

			return actions, ingredients, tools
		
		def convert_fraction(self, word):
			if self.is_vulgar_fraction(word[-1]):
		
				number = unicodedata.numeric(word[-1])
				if len(word) > 1:
					if word[:-2].isnumeric():
						number += float(word[:-2])
					else:
						return word
		
				return str(int(number)) if number%1==0 else str(round(float(number), 2))
		
			elif re.match(r'[0-9]+/[0-9]+', word):
				word = word.split('/')
				return str(round(float(word[0]) / float(word[1]), 2))
		
			return word
		
		def is_vulgar_fraction(self, character):
			try:
				unicodedata.numeric(character)
				try:
					float(character)
					return False
				except ValueError:
					return True
			except ValueError:
				return False

		# Returns the time component of the step, or unknown
		def get_time(self):

			seconds = re.compile(r'[1-9]+[0-9]* [sS]econds?')
			minutes = re.compile(r'[1-9]+[0-9]* [mM]inutes?')
			hours = re.compile(r'[1-9]+[0-9]* [hH]ours?')

			for time_pattern in [seconds, minutes, hours]:
				match = time_pattern.search(self.text)
				if match:
					start = match.span()[0]
					end = match.span()[1]
					
					return self.text[start:end]

			return 'None Specified'
        
		def get_temp(self):
			temp = re.compile(r'[1-9]+[0-9]* [dD]egrees? [CF]')
			temp2 = re.compile(r'[rR]oom [tT]emperature')
			
			for temp_pattern in [temp, temp2]:
				match = temp_pattern.search(self.text)
				if match:
					start = match.span()[0]
					end = match.span()[1]
					return self.text[start:end]
				
		def get_quantities(self):
			quantities = []
			# this is not done yet
			return quantities
            

	def __init__(self, url):

		# Store raw HTML
		html_doc = request.urlopen(url)
		self.soup = bs(html_doc, 'html.parser')

		# Getting the Recipe name
		title = self.soup.find('title')
		if ' | Allrecipes' in title.text:
			title = title.text[:-13]

		self.recipe_name = title

		# Getting the ingredients
		self.ingredients = self.get_ingredients()

		# All of the text for a recipe's steps
		self.text = [div.text for div in self.soup.find_all('div', {'class': 'paragraph'})]

		# Parsing the steps
		self.steps = self.get_steps()

		# Getting tools and actions
		self.tools = self.named_tools()
		self.potential_main_actions = self.pmActions()
		self.main_actions = self.mActions()

	def find_tags(self):
		find_tag_list = self.soup.find('script', id='karma-loader')
		find_tag_list = str(find_tag_list).split()
		append_to_list = False
		tags = []
		for item in find_tag_list:
		    item = item.replace('"','')
		    item = item.replace(',','')
		    if append_to_list and '[' not in item:  
		        if ']' in item:
		            break
		        tags.append(item)
		    if 'tags:' == item:
		        append_to_list = True
		return tags

	#Identifies Potential Main Actions:
	def pmActions(self):
		first_words = []
		potential_main_actions = []
		for step in self.steps:
			each_step = step.text.split()
			first_words.append(each_step[0])
		for word in first_words:
			if word.lower() in data.cooking_methods:
				potential_main_actions.append(word)
		pma = []
		for i in potential_main_actions:
			if i.lower() not in pma:
				pma.append(i.lower())
		return pma

	#Identifies Likely main actions
	def mActions(self):
		action_list = ['cook', 'bake', 'fry', 'roast', 'grill', 'steam', 'poach', 'simmer', 'broil', 'blanch', 'braise', 'stew']
		main_actions = []
		for action in self.potential_main_actions:
			if action.lower() in action_list:
				main_actions.append(action)
		ma = []
		for i in main_actions:
			if i.lower() not in ma:
				ma.append(i.lower())
		return ma

	def named_tools(self):
		tools = []
		for step in self.steps:
			for tool in data.tools:
				if tool in step.text:
					tools.append(tool)
		t = []
		for i in tools:
			if i.lower() not in t:
				t.append(i.lower())
		return t


	@staticmethod
	def clean_split(string, seps):
		result = [string]
		for sep in seps:
			new = result[:]
			result = []
			for phrase in new:
				new_phrase = phrase.split(sep)
				if sep.isalpha() and len(new_phrase) > 1:
					new_phrase = [new_phrase[0]] + [sep + x for x in new_phrase[1:]]
				result += new_phrase

		if result[-1].strip() == 'or':
			result = result[:-1]
		return [x.strip() for x in result if x != ' ']

	# Given a list of words, cleans substeps of phrases that contain those words
	def clean_substeps(self, to_clean):
		# Getting substeps
		cleaned = []
		for i, step in enumerate(self.steps):
			substeps = step.text.split('.')
			for j, substep in enumerate(substeps):
				phrases = self.clean_split(substep, [',', ';', 'until', ', and'])
				for word in to_clean:
					phrases = [phrase for phrase in phrases if word not in phrase]
				substeps[j] = ', '.join(phrases)
				if 'should read' in substeps[j] and 'degree' in substeps[j] and 'thermometer' not in substeps[j]:
					substeps[j] = ''

			step = '. '.join(substeps)
			if len(step.strip()) == 0:
				self.steps[i].new_text = ''
			else:
				cleaned.append(step)
				self.steps[i].new_text = step
		self.steps = [s for s in self.steps if s.new_text != '']
		return cleaned

	# Ingredient Parser
	def get_ingredients(self):

		# Getting all span texts with ingredients-item-name
		ingredient_strings = self.soup.find_all('span', {'class': 'ingredients-item-name'})
		ingredient_strings = [span.text.lower() for span in ingredient_strings]

		# Cleaning the ingredients
		ingredients = []
		unknown = {}
		ingredient_indices = {}
		index = 0
		for string in ingredient_strings:

			# Replacing thin spaces
			string = string.replace('\u2009', '')

			# Ingredient structure
			ingredient = {
				'name': '',
				'type': 'NULL',
				'quantity': .0,
				'measurement': '',
				'descriptors': [],
				'prep': []
			}

			# Very special case
			if 'to taste' in string:
				string = string.replace('to taste', 'to|taste')

			# Parsing out descriptors in parentheses
			parens = re.search(r'(\([^\)]+\))', string)
			if parens:
				for paren in parens.groups():
					ingredient['descriptors'].append(paren[1:-1])
					string = string.replace(paren, '')
					string = string.replace('  ', ' ')

			# Determining a 'split word'
			split_word = ''
			for word in string.split():
				if word in data.all_ingredients:
					split_word = word
					break

			# Removing commas before the split word
			if split_word:
				string = string.split(split_word)

				# Decomposing into before and after components for processing
				before = string[0].replace(',', ' ') + split_word
				after = ' '.join(string[1:]).replace('  ', ' ')

				# Getting 'in x' as a prep step after the split
				if ' in ' in after:
					after = after.split(' in ')
					after_before = after[0]
					after_after = ' '.join(['in'] + after[1:])
					ingredient['prep'].append(after_after)
					after = after_before

				# Rebuilding string
				string = ' '.join([before, after])

			# Determining if the ingredient has 'prep steps'
			string = string.split(',')
			if len(string) > 1:
				ingredient['prep'] = [' '.join(string[1:]).strip()]

			string = string[0]
			string = string.split(' - ')
			if len(string) > 1:
				ingredient['prep'] = [' '.join(string[1:]).strip()]

			# Determining if the ingredient has an explicit quantity
			string = string[0].split()
			has_quantity = False
			for i, word in enumerate(string):

				# Catching more preparatory steps
				if word.endswith('ed') and word != 'red':
					if i > 0 and isinstance(string[i-1], str) and string[i-1].endswith('ly'):
						ingredient['prep'].append(f'{string[i-1]} {word}')
						string[i-1] = None
					else:
						ingredient['prep'].append(word)
					string[i] = None

				if word.endswith('less'):
					ingredient['descriptors'].append(word)
					string[i] = None

				# Replacing 'A and a' with 1
				if word.lower() == 'a':
					word = '1'
					string[i] = '1'

				# Checking for numbers
				try:
					number = self.convert_fraction(word)
					string[i] = number
					has_quantity = True
				except ValueError:
					continue

			# Removing null words that were added as prep
			string = [x for x in string if x is not None]

			# If the string has an explicit quanity
			if has_quantity:
				if len(string) == 1:
					ingredient['name'] = string[0]
				elif len(string) == 2:
					ingredient['quantity'] = string[0]
					ingredient['measurement'] = 'whole'
					ingredient['name'] = string[1]
				else:
					ingredient['quantity'] = string[0]
					ingredient['measurement'] = string[1]
					ingredient['name'] = ' '.join([str(x) for x in string[2:]])


			# Special cases where there is no quantity
			else:
				ingredient['name'] = ' '.join(string)
				unknown[ingredient['name']] = ingredient

			# This initial parse will properly handle most ingredients, but the validation step is necessary to improve accuracy for the others
			ingredients.append(self.validate(ingredient))
			ingredient_indices[ingredient['name']] = index
			index += 1

		return ingredients


	# Given a vulgar fraction string, returns a float
	def convert_fraction(self, string_fraction):
		if len(string_fraction) == 1:
			return unicodedata.numeric(string_fraction)
		else:
			return sum([self.convert_fraction(c) for c in string_fraction])

	# Validates the legitimacy/accuracy of an ingredient parse, returning a modified ingredient
	def validate(self, ingredient):

		# Validating measurements
		if ingredient['measurement'] not in data.measurements:
			name = ingredient['measurement'] + ' ' + str(ingredient['name'])
			for word in name.split():
				if word in data.measurements or word[:-1] in data.measurements:
					ingredient['measurement'] = 'to taste' if word == 'to|taste' else word
					ingredient['name'] = name.replace(word, '').replace('  ', ' ').strip()
					break
			else:
				ingredient['name'] = name
				ingredient['measurement'] = 'whole'

		# Validating ingredients, getting type information
		for ingredient_type in data.ingredients_list:
			if ingredient['name'] in data.ingredients_list[ingredient_type]:
				ingredient['type'] = ingredient_type
				break

		# Ingredient type not found, checking individual words
		else:
			for word in reversed(ingredient['name'].split()):
				found = False

				for ingredient_type in data.ingredients_list:
					ingredients = data.ingredients_list[ingredient_type]
					if word in ingredients or word[:-1] in ingredients:
						ingredient['type'] = ingredient_type
						found = True
						break

				if found:
					break

		# Identifying 'descriptors'
		per_word = [token.text for word in ingredient['name'].split() for token in nlp(word) if token.pos_ == 'ADJ']

		per_whole = [token.text for token in nlp(ingredient['name']) if token.pos_ == 'ADJ']

		for word in ingredient['name'].split():
			if word in per_word or word in per_whole:
				ingredient['descriptors'].append(word)

		return ingredient

	# Returns a step graph
	def get_steps(self):

		# Getting all the text corresponding to steps
		steps = [div.text for div in self.soup.find_all('div', {'class': 'paragraph'})]

		# Substeps are sentence level
		substeps = []
		for step in steps:
			substeps += [x.strip() for x in step.split('.')]

		# Creating a step for each sentence
		steps = [self.Step(x) for x in substeps]
		steps = [s for s in steps if len(s.text) > 0]

		# Im not sure
		'''
		for i, step in enumerate(self.steps):
			for ing, _ in enumerate(self.ingredients):
				if ing in step.text and ing not in step.ingredients:
					self.steps[i].ingredients.append(ing)
		'''

		return steps
	def output_ingredients(self):
			print("Ingredients: ")
			for info in self.ingredients:
				if info['quantity'] == 0.0:
					print(info['name'], info['measurement'])
				else:
					prep_string = ', '.join(info['prep'])
					if len(prep_string) > 0:
						prep_string = ', ' + prep_string
					descriptors_not_in_name = [d for d in info['descriptors'] if d not in info['name']]
					d = ' ' + ', '.join(descriptors_not_in_name)
					if len(d) == 1:
						d = ''
					q = info['quantity']
					if q % 1 == 0.0:
						q = str(int(q))
					else:
						q = str(q)
					m = '' if info['measurement'] == 'whole' else info['measurement']
					n = info['name']
					if len(m) == 0:
						print(q + d, n + prep_string)
					else:
						print(q + d, m, n + prep_string)

# Returns a valid recipe url based on an integer input
def get_recipe_url(num=259356):
	response = requests.get(f'https://www.allrecipes.com/recipe/{num}')
	if response.status_code == 200:
		return response.url
	return get_recipe_url(259356)