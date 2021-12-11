from copy import deepcopy
import pandas as pd
import data
import re

replacements = {
	'measurement': data.measurements,
	'action': data.cooking_methods,
	'tool': data.tools,
	'food': data.all_ingredients 
}

# A class that can use a formatted string as a way to generate more strings of natural language
class Template():

	def __init__(self, string):

		self.template = string
		self.replacements = self._get_replacements()
		self.current = string
		self.remaining = deepcopy(self.replacements)
		self.exhausted = False

	# INTERNAL USE ONLY
	def _get_replacements(self):
		pattern = re.compile(r'\([^)]+\)')

		matches = []
		for i, m in enumerate(pattern.finditer(self.template)):
			s = m.start()
			e = m.end()

			match = {
				'string': m.string[s:e],
				'span': (s, e),
				'length': e - s,
				's_index': i,
				'r_index': 0
			}

			matches.append(match)

		return matches

	# INTERNAL USE ONLY
	def _replace(self, index, replacement):
		r = self.remaining[index]
		others = [x for x in self.remaining if x['s_index'] > r['s_index']]

		start = r['span'][0]
		end = r['span'][1]

		self.current = self.current[:start] + replacement + self.current[end:]

		length = len(replacement)
		r['string'] = replacement
		r['span'] = (start, start + length)

		diff = length - r['length']
		r['length'] = length

		for r in others:
			start = r['span'][0]
			end = r['span'][1]
			r['span'] = (start + diff, end + diff)

	# Generates a string from the template
	def generate(self):

		# Resetting if the template has been exhausted
		if self.exhausted:
			self.reset()

		# Replacing all replacements
		for i, r in enumerate(self.remaining):
			key = r['string'][1:-1]
			replacement = replacements[key][r['r_index']]
			self._replace(i, replacement)

		# Iterating through replacement indices
		for i, r in enumerate(self.replacements):
			key = r['string'][1:-1]
			if r['r_index'] < len(replacements[key]) - 1:
				r['r_index'] += 1

				# Making sure that all of the indexes before get reset
				for r2 in self.replacements[:i]:
					r2['r_index'] = 0

				break

		# If we can not increment any replacement index, we have run out of novel replacements: Exhausted
		else:
			self.exhausted = True

		# what we want to return
		generated = self.current

		# Resetting template state for the next generation
		self.current = self.template
		self.remaining = deepcopy(self.replacements)

		return generated

	# Generated n samples
	def generate_n(self, n):
		return [self.generate() for _ in range(n)]

	# Generate until this templatae is exhausted
	def generate_all(self):
		generated = []
		while not self.exhausted:
			generated.append(self.generate())

		return generated

	# Reset template to default state
	def reset(self):
		for r in self.replacements:
			r['r_index'] = 0
		self.exhausted = False



# One for each intent we are trying to categorize
class Category():

	def __init__(self, name, template_strings, index=[0]):

		self.name = name
		self.index = index[0]
		index[0] += 1
		self.templates = [Template(string) for string in template_strings]

	# Given a value n, returns a list of n strings of natural language generated from the category's templates.
	def generate(self, n=0):

		template_n = int(n / len(self.templates)) + 1
		result = [string for template in self.templates for string in template.generate_n(template_n)]

		return result[:n]
			



# Given a list of categories, returns a dataset containing n randomized samples from each category
def create_dataset(categories, n):
	dataset = pd.DataFrame(columns=['text', 'label'])

	texts = []
	labels = []

	for category in categories:
		texts += category.generate(n)
		labels += [category.name for _ in range(n)]

	dataset['text'] = texts
	dataset['label'] = labels

	return dataset


def main():

	from agent import Intent
	intents = [intent.value for intent in Intent]

	pairs = []
	for intent in intents:
		try:
			pairs.append((intent, getattr(data, intent)))
		except AttributeError:
			continue


	categories = [Category(name, templates) for name, templates in pairs]

	dataset = create_dataset(categories, 300)

	print(dataset)

	dataset.to_csv('training_data.csv')


if __name__ == '__main__':
	main()

