from transformers import AutoTokenizer, \
						 AutoModel, \
						 BertTokenizer, \
						 BertForSequenceClassification

import pandas as pd
import numpy as np
import torch
import pickle

class Model():

	def __init__(self):

		with open('./saved_model/labels_categories.p', 'rb') as f:
			self.labels_to_categories = pickle.load(f)

		with open('./saved_model/category_labels.p', 'rb') as f:
			self.categories_to_labels = pickle.load(f)

		self.max_len = 32

		directory = './saved_model'
		model = BertForSequenceClassification.from_pretrained(
		                directory,
		                local_files_only=True,
		                num_labels=len(self.labels_to_categories),
		                output_attentions=False,
		                output_hidden_states=False
		                                                      )

		if torch.cuda.is_available():
			model.cuda()
			self.device = torch.device('cuda')
		else:
			self.device = torch.device('cpu')

		model.eval()

		self.classifier = model

		self.tokenizer = BertTokenizer.from_pretrained(directory, do_lower_case=True)

	def __call__(self, text):

		tokens = self.tokenizer.encode_plus(
		                text,
		                add_special_tokens=True,
		                max_length = self.max_len,
		                truncation=True,
		                padding='max_length',
		                return_attention_mask=True,
		                return_tensors='pt'
		                                    )

		tokens = tokens['input_ids'].to(self.device)
		logits = self.classifier(tokens).logits
		logits = logits.detach().cpu().numpy()
		result = torch.argmax(torch.tensor(logits)).item()

		return self.labels_to_categories[result]


def main():
	model = Model()
	print(model('show ingredients'))
	print(model('hehexd'))

if __name__ == '__main__':
	main()




