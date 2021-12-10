from transformers import pipeline, \
						 BertTokenizer, \
						 BertForSequenceClassification, \
						 AdamW, \
						 BertConfig, \
						 get_linear_schedule_with_warmup

from torch.utils.data import TensorDataset, \
							 random_split, \
							 DataLoader, \
							 RandomSampler, \
							 SequentialSampler

import torch
import pandas as pd
import numpy as np

dataset = pd.read_csv('./training_data.csv').astype('string')
dataset = dataset.sample(frac=1)
dataset = dataset.sample(frac=1)
dataset = dataset.sample(frac=1)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

input_ids = []
attention_masks = []
max_len = 32

for text in dataset['text']:
	inp = tokenizer.encode_plus(
	                            text, 
	                            add_special_tokens=True,
	                            max_length = max_len,
	                            truncation = True,
	                            padding= 'max_length',
	                            return_attention_mask = True,
	                            return_tensors = 'pt'
	                            )
	# Grabbing the input components (encoded_plus gives us a dict with attention_mask)
	input_ids.append(inp['input_ids'])
	attention_masks.append(inp['attention_mask'])

# Conversion to tensors
input_ids = torch.cat(input_ids, dim=0)
attention_masks = torch.cat(attention_masks, dim=0)

# Creating labels
category_labels = {c: i for i, c in enumerate(set(dataset['label'].to_list()))}
labels_categories = {v: k for k, v in category_labels.items()}
dataset['number_label'] = dataset['label'].map(lambda c: category_labels[c])
labels = dataset['number_label'].to_list()
labels = torch.tensor(labels)


# Combine the training inputs into a TensorDataset.
training_dataset = TensorDataset(input_ids, attention_masks, labels)

# Define a proportion of the data to set as test v train (0.9 = 90% train)
proportion = 0.9

# Calculate the number of samples to include in each set.
train_size = int(proportion * len(training_dataset))
val_size = len(training_dataset) - train_size

# Divide the dataset by randomly selecting samples.
train_dataset, val_dataset = random_split(training_dataset, [train_size, val_size])

print(f'Training samples: {train_size}')
print(f'Validation samples: {val_size}')

# Dataloaders need a batch size (32 recommended)
batch_size = 16

train_dataloader = DataLoader(
            train_dataset,  # The training samples.
            sampler = RandomSampler(train_dataset), # Select batches randomly
            batch_size = batch_size # Trains with this batch size.
        )

validation_dataloader = DataLoader(
            val_dataset, # The validation samples.
            sampler = SequentialSampler(val_dataset), # Pull out batches sequentially.
            batch_size = batch_size # Evaluate with this batch size.
        )

# Defining our model
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels = len(category_labels),
    output_attentions = False,
    output_hidden_states = False
)

# Determining total steps
epochs = 10
total_steps = len(train_dataloader) * epochs

optimizer = AdamW(model.parameters(), lr = 2e-5, eps = 1e-8)

scheduler = get_linear_schedule_with_warmup(optimizer, 
                                            num_warmup_steps = 0,
                                            num_training_steps = total_steps)

# Determining if we have a GPU to use
if torch.cuda.is_available():
	model.cuda()
	device = torch.device("cuda")
else:
	device = torch.device("cpu")


# Function to calculate the accuracy of our predictions vs labels
def flat_accuracy(preds, labels):
	pred_flat = np.argmax(preds, axis=1).flatten()
	labels_flat = labels.flatten()
	return np.sum(pred_flat == labels_flat) / len(labels_flat)


# Graphing stats later
training_stats = []

# The training loop
for epoch in range(epochs):

	total_training_loss = 0
	model.train()

	for step, batch in enumerate(train_dataloader):
		print(f'Step {step} of {len(train_dataloader)}', end='\r', flush=True)

		# Decomposing the batch
		b_input_ids = batch[0].to(device)
		b_input_mask = batch[1].to(device)
		b_labels = batch[2].to(device)

		# Resetting gradient accumulation
		model.zero_grad()

		# Getting model outputs
		result = model(b_input_ids, 
		               token_type_ids = None, 
		               attention_mask = b_input_mask, 
		               labels = b_labels,
		               return_dict = True)

		# Decomposing the model output
		loss = result.loss
		logits = result.logits

		# Accumulating training loss
		total_training_loss += loss.item()

		# Gradient calculation
		loss.backward()

		# Preventing exploding gradients
		torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

		# Updating weights
		optimizer.step()

		# Updating the optimizer learning rate
		scheduler.step()

	# Epoch Completed
	avg_train_loss = total_training_loss / len(train_dataloader)

	# Setting the mode again. Opposite of model.train()
	model.eval()

	# Tracking some stats
	total_eval_accuracy = 0
	total_eval_loss = 0
	nb_eval_steps = 0

	for batch in validation_dataloader:

		b_input_ids = batch[0].to(device)
		b_input_mask = batch[1].to(device)
		b_labels = batch[2].to(device)

		with torch.no_grad():

			result = model(b_input_ids, 
                     token_type_ids = None, 
                     attention_mask = b_input_mask,
                     labels = b_labels,
                     return_dict = True)
      
		loss = result.loss
		logits = result.logits

		total_eval_loss += loss.item()

		# Bringing GPU calculations back to the CPU
		logits = logits.detach().cpu().numpy()
		label_ids = b_labels.to('cpu').numpy()

		total_eval_accuracy += flat_accuracy(logits, label_ids)

	avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
	print(f'\nAccuracy on validation: {avg_val_accuracy}')

	avg_val_loss = total_eval_loss / len(validation_dataloader)
	print(f'Loss on validation: {avg_val_loss}')

	training_stats.append(
	                    {
            'epoch': epoch + 1,
            'Training Loss': avg_train_loss,
            'Valid. Loss': avg_val_loss,
            'Valid. Accur.': avg_val_accuracy
            }
            )


def test_model(string):
  tokens = tokenizer.encode_plus(
	                            string, 
	                            add_special_tokens=True,
	                            max_length = max_len,
	                            truncation = True,
	                            padding= 'max_length',
	                            return_attention_mask = True,
	                            return_tensors = 'pt'
	                            )['input_ids'].to(device)
  
  logits = model(tokens).logits
  logits = logits.detach().cpu().numpy()
  best = torch.argmax(torch.tensor(logits)).item()

  return labels_categories[best]

shuffled = dataset.sample(frac=1)

print(category_labels, '\n')
for i, row in enumerate(shuffled.iterrows()):
  text, label = row[1]['text'], row[1]['label']
  print(label == test_model(text))
  if i > 1000:
    break