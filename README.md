# Instructions

To run our conversational agent, please create a new python virtual environment, and then pip install our requirements:

 - pip install -r requirements.txt

Then, from within the SRC directory, please run the following command

 - python agent.py

This will begin the conversation with the conversational bot.

We have different types of commands
	START = 'start'
   using a start command will allow you to begin working through a recipe. After choosing a start command you will be prompted to provide the URL from all recipes.
	SHOW = 'show'
   using a show command will show you things like: the ingredients list, the list of steps, the name of the recipe.
	NAVIGATE = 'navigate'
	SEARCH = 'search'
	GET_PARAM = 'get_param'
	SUBSTITUTE = 'substitute'
	QUIT = 'quit'
	ACKNOWLEDGE = 'acknowledge'
	UNKNOWN = 'unknown'
