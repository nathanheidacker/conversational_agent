# Recipe-Parsing Conversational Agent

Github link: https://github.com/nathanheidacker/conversational_agent

Welcome to our conversational agent! This bot parses any recipe from [allrecipes.com](https://www.allrecipes.com/), and will guide you through it using natural conversation.

This agent uses an intent classifier on top of a a pretrained transformer (BERT) to categorize the intent of the user during conversation and perform the corresponding action.

## Installation / Setup

To run our conversational agent, please create and activate a new python virtual environment, and then pip install our requirements:

 - pip install -r requirements.txt

Next, please download and unzip the zip file contained in [this google drive](https://drive.google.com/drive/folders/11clkg2tyr3cdlmD3SV8FcWHoZTq_YDYH?usp=sharing). In the unzipped contents, there should be a directory called saved_model. Unfortunately, the size is over 400MB, so we are unable to deliver it by email or on GitHub. This contains our BERT intent classifier's model weights and tokenizer information. Drop the entire saved_model directory inside of the src folder. The resulting path should look like './conversational_agent/src/saved_model/'.

Then, from within the SRC directory, please run the following command

 - python agent.py

This will begin the conversation with the conversational bot.

## Instruction Manual

Our bot has 2 fundamentally different modes of interaction. 

The first and most obvious is a natural language parser (using the BERT classifier) that will interpret the intent of any natural language input. Simply enter any query, and the bot will try to interpret the intent and then carry out the corresponding action.

NOTE: The maximum input tensor length is 32 tokens, so keep queries short (30 words or less typically).

Because we had a very limited means of building out our training data, this model is often flawed, and will misinterpret the intent of a query. If you want to test the results of a query on a specific intent (even one that doesn't match the actual intent), you can do so by prepending a '!intent' to the beginning of your query. The text coming after the !intent (separated by a space) will instead by interpreted as the query, corresponding to the intent contained within the !intent. Below are some examples to illustrate:

 - !search how do I preheat an oven
 - !navigate show me the next step
 - !show how long does this recipe take

 There are 8 different intents on which the model was trained, as well as 1 which is automatic (quitting/terminating the program). They are as follows

  - START: begin a new recipe
  - SHOW: see information regarding the recipe as a whole
  - NAVIGATE: see the next or previous step, navigate through the recipe steps
  - SEARCH: find general information or information unavailable to us through the recipe alone.
  - GET_PARAM: see some information about the current step, or an ingredient in the recipe
  - SUBSTITUTE: find a reasonable substitute for an ingredient
  - QUIT: terminate the program
  - UNKNOWN: the user's intent is unrecognized, or unsatisfiable
  - ACKNOWLEDGE: the user has no specific intent

Examples of !intent commands corresponding to each of these are provided below:

 - !start lets make something
 - !show what are the ingredients
 - !navigate what was the previous step
 - !search how do I roast a chicken
 - !get_param how much should I use
 - !substitute whats a good replacement for rosemary
 - !quit (terminates the program regardless of query)
 - !unknown (same reponse regardless of query)
 - !acknowledge (same response regardless of query)
