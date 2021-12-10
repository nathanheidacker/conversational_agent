volume_measurements = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tbs.', 'tbsp.', 'fluid ounce', 'fl oz', 'gill', 'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g' 'gal', 'ml', 'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre', 'dL']

mass_measurements = ['pound', 'lb', '#', 'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme']

length_measurements = ['mm', 'millimeter', 'millimetre', 'cm', 'centimeter', 'cenimetre', 'm', 'meter', 'metre', 'inch', 'in', '\"', 'thin']

size_measurements = ['small', 'medium', 'large', 'extra large', 'whole']

nonstandard_measurements = ['pinch','can', 'stick', 'handful', 'dash', 'to|taste', 'container', 'package', 'loaf', 'slices']

measurements = volume_measurements + mass_measurements + length_measurements + size_measurements + nonstandard_measurements


cooking_methods = ['bake', 'fry', 'stir', 'roast', 'sautee', 'microwave', 'broil', 'poach', 'boil', 'reduce', 'add', 'combine', 'grill', 'steam', 'simmer', 'blanch', 'braise', 'mix', 'sear', 'blend', 'turn', 'brush', 'place', 'preheat', 'smoke', 'break', 'melt', 'spread', 'layer', 'roll out', 'peel', 'cut', 'chop', 'pinch', 'pour', 'weigh', 'measure', 'knead', 'quarter', 'cube', 'slice', 'carve', 'grate', 'squeeze', 'sprinkle', 'cook', 'chill']


tools = ['baking pan','baking sheet','barbecue grill','baster','basting brush','blender','bread basket','bread knife','Bundt pan','butcher block','cake pan','can opener','carafe','casserole pan','charcoal grill','cheese cloth','coffee maker','coffee pot','colander','convection oven','cookbook','cookie cutter','cookie press','cookie sheet','cooling rack','corer','crepe pan','crock','crock pot','cupcake pan','custard cup','cutlery','cutting board','Dutch oven','egg beater','egg poacher','egg timer','espresso machine','fondue pot','food processor','fork','frying pan','garlic press','gelatin mold','grater','griddle','grill pan','grinder','hamburger press','hand mixer','honey pot','ice bucket','ice cream scoop','icing spatula','infuser','jar opener','jellyroll pan','juicer','kettle','knife','ladle','lasagne pan','lid','mandolin','measuring cup','measuring spoon','microwave oven','mixing bowl','mold','mortar and pestle','muffin pan','nut cracker','oven','oven mitts','pan','parchment paper','paring knife','pastry bag','peeler','pepper mill','percolator','pie pan','pitcher','pizza cutter','pizza stone','platter','poacher','popcorn popper','pot','pot holder','poultry shears','pressure cooker','quiche pan','raclette grill','ramekin','refrigerator','rice cooker','ricer','roaster','roasting pan','rolling pin','salad bowl','salad spinner','salt shaker','sauce pan','scissors','sharpening steel','shears','sieve','skewer','skillet','slicer','slow cooker','souffle dish','spice rack','spoon','steak knife','steamer','stockpot','stove','strainer','tablespoon','tart pan','tea infuser','teakettle','teaspoon','thermometer','toaster','toaster oven','tongs','trivet','utensils','vegetable bin','vegetable peeler','waffle iron','water filter','whisk','wok','yogurt maker','zester']

cooking_mediums = ['water', 'olive oil', 'butter', 'vegetable oil', 'margarine']

fats = ['olive oil', 'butter', 'vegetable oil', 'margarine', 'oil', 'lard']

proteins = ['beef', 'lamb', 'veal', 'pork', 'kangaroo', 'chicken', 'turkey', 'duck', 'emu', 'goose', 'fish', 'prawn', 'crab', 'lobster', 'mussels', 'oyster', 'scallop', 'clams', 'shrimp', 'milk', 'yogurt', 'yoghurt', 'cheese', 'cottage cheese', 'almond', 'pine nut', 'walnut', 'macadamia', 'hazelnut', 'cashew', 'pumpkin seed', 'sesame seed', 'sunflower seed', 'bean', 'lentil', 'chickpea', 'split pea', 'tofu', 'bacon', 'chia seed', 'egg', 'egg whites', 'cod', 'halibut', 'salmon', 'sardine', 'tilapia', 'hemp seed', 'hummus', 'peanut butter', 'peanut', 'pork chop', 'whey', 'protien powder', 'tenderloin', 'refried bean', 'turkey bacon', 'bush birds']

vegetarian_proteins = ['milk', 'yogurt', 'yoghurt', 'cheese', 'cottage cheese', 'almond', 'pine nut', 'walnut', 'macadamia', 'hazelnut', 'cashew', 'pumpkin seed', 'sesame seed', 'sunflower seed', 'bean', 'lentil', 'chickpea', 'split pea', 'tofu', 'chia seed', 'egg', 'egg whites', 'hemp seed', 'hummus', 'peanut butter', 'peanut', 'whey', 'protein powder', 'refried bean']

meat_proteins = ['beef', 'lamb', 'veal', 'pork', 'kangaroo', 'chicken', 'turkey', 'duck', 'emu', 'goose', 'bush birds', 'fish', 'prawn', 'crab', 'lobster', 'mussels', 'oyster', 'scallop', 'clams', 'shrimp', 'bacon', 'cod', 'halibut', 'salmon', 'tilapia', 'pork chop', 'protien powder', 'tenderloin', 'turkey bacon', 'sardine']

lean_proteins = ['duck', 'emu', 'goose', 'bush birds', 'chicken', 'turkey', 'pheasant', 'rabbit']

nuts_and_seeds = ['nut', 'seed', 'pecan', 'hazelnut', 'coconut', 'almond', 'chestnut', 'macadamia', 'cashew', 'walnut', 'peanut', 'peanut butter']

vegetables = ['amaranth leaves','amaranth','arrowroot','artichoke','arugula','asparagus','avocado','bamboo shoot','bamboo','beet','belgian endive','bell pepper','bitter melon','bok choy','borage','breadfruit','broad bean','broadbean','broccoli','broccoli rabe','brussel sprout','Brussels sprouts','burdock','butternut squash','cabbage','caper','cardoon','carrot','cassava','cauliflower','celeriac','celery','celery root','chard','chayote','chickpea','chicory','chinese water chestnut','collard','common bean','corn','cowpea','crookneck','cucumber','curly endive','daikon','dandelion','dock','durian','edamame','eggplant','endive','fava bean','fennel','fiddlehead','gherkin','ginger','grapeleaves ','grean pea','green bean','green cabbage','green pepper','horseradish','husk tomato','iceberg lettuce','Indian fig','jackfruit','Jerusalem artichoke','jicama','jícama','kale','kohlrabi','lamb’s lettuce','lamb’s quarters','leek','lemongrass','lentil','lettuce','lettuce leaf','lima bean','loofah','lotus','moringa','mushroom','musk cucumber','mustard green','Napa cabbage','okra','olive','onion','orange pepper','oysterplant','parsnip','pea','peanut','pepper','plantain','potato','pumpkin','radicchio','radish','red cabbage','red onion','red pepper','red potato','romaine','romaine lettuce','rutabaga','salsify','shallot','snake gourd','snap peas','snow pea','sorrel','soybean','spaghetti squash','spinach','squash','squashblossoms ','sugar snap peas','sweet potato','sweet red pepper','swiss chard','taro','ti','tomatillo','tomato','Tossa jute','turnip','water chestnut','watercress','wax gourd','white potato','yam','yam root','yellow pepper','yellow potato','yuca root','zucchini']

fruits = ['acerola', 'west indian cherry', 'apple', 'apricots', 'avocado', 'banana', 'blackberry', 'blackcurrant', 'blueberry', 'breadfruit', 'cantaloupe', 'carambola', 'cherimoya', 'cherry', 'clementine', 'coconut', 'coconut meat', 'cranberry', 'custard-apple', 'date', 'date fruit', 'durian', 'elderberry', 'feijoa', 'fig', 'gooseberry', 'grapefruit', 'grape', 'guava', 'honeydew melon', 'melon', 'jackfruit', 'java-plum', 'plum', 'jujube fruit', 'kiwi', 'kiwifruit', 'kumquat', 'lemon', 'lime', 'lingonberry', 'longan', 'loquat', 'lychee', 'mandarin', 'mandarin orange', 'mango', 'mangosteen', 'mulberry', 'nectarine', 'olive', 'orange', 'papaya', 'passion fruit', 'peach', 'pear', 'persimmon', 'pitaya', 'dragonfruit', 'pineapple', 'pitanga', 'plantain', 'pomegranate', 'prickly pear', 'prune', 'pummelo', 'quince', 'raspberry', 'rhubarb', 'rose-apple', 'sapodilla', 'mamey sapote', 'sapote', 'soursop', 'strawberry', 'sugar-apple', 'tamarind', 'tangerine', 'watermelon']

seasonings = ['allspice','angelica','anise','asafoetida','bay leaf','basil','bergamot','black cumin','black mustard','black pepper','borage','brown mustard','burnet','caraway','cardamom','cassia','catnip','cayenne pepper','celery seed','chervil','chicory','chili pepper','chives','cicely','cilantro','cinnamon','clove','coriander','costmary','cumin','curry','dill','fennel','fenugreek','filé','ginger','grains of paradise','holy basil','horehound','horseradish','hyssop','lavender','lemon balm','lemon grass','lemon verbena','licorice','lovage','mace','marjoram', 'mustard', 'nutmeg','oregano','paprika','parsley','peppermint','poppy seed','rosemary','rue','saffron','sage','savory','sesame','sorrel','star anise','spearmint','tarragon','thyme','turmeric','vanilla','wasabi','white mustard','salt', 'pepper', 'paste', 'lemon juice', 'lime juice', 'soy sauce', 'juice', 'zest', 'garlic', 'flakes', 'syrup', 'molasses', 'balsamic', 'sugar', 'extract']

binders = ['egg', 'cracker', 'cracker crumb', 'oatmeal', 'rice', 'milk', 'evaporated milk', 'gelatin', 'guar gum', 'xanthan gum', 'psyllium husk', 'potato starch', 'cornstarch']

starches = ['ciabatta', 'french bread', 'whole wheat bread', 'sourdough', 'rye bread', 'pita bread', 'focaccia', 'multigrain', 'brioche', 'bread', 'waffle', 'english muffin', 'dough', 'flour', 'pasta', 'noodle', 'pastry']

sauces = ['sauce', 'mayo', 'mayonnaise']

meat_words = ['bone', 'skin', 'blood', 'juice run', 'juices run', 'pink', 'meat', 'cavity', 'thigh', 'breast', 'fish']
lactose_milks = ['goat\'s milk', 'buffalo milk', 'cow\'s milk', 'fresh sour milk', 'kefir', 'skyr', 'buttermilk', 'condensed milk', 'evaporated milk', 'lactose', 'milk byproduct', 'milk casein', 'milk powder', 'milk sugar', 'powdered milk', 'whey', 'whey protein concentrate', 'milk']
lactose_creams =  ['heavy cream', 'cream', 'ice cream', 'sour cream', 'whipped cream', 'yogurt', 'yoghurt', 'curd']
lactose_cheeses = ['cream cheese', 'cottage cheese', 'mozzarella cheese', 'ricotta cheese', 'cheese']
avoid_butters = ['peanut butter', 'sun butter', 'almond butter', 'nut butter']
milk_alternates = ['soy milk', 'rice milk', 'almond milk', 'coconut milk', 'cashew milk', 'oat milk', 'hazelnut milk']
cream_alternates = ['soy cream', 'cashew cream', 'pureed tofu', 'pureed beans', 'olive oil']
cheese_alternates = ['kite hill ricotta', 'soy cheese', 'cashew cheese', 'zucchini cheese','daiya cheese', 'tahini spread']
ingredients_list = {
	'cooking_medium': cooking_mediums,
	'protein': proteins,
	'nuts_and_seeds': nuts_and_seeds,
	'seasoning': seasonings,
	'vegetable': vegetables,
	'binder': binders,
	'starch': starches,
	'fruit': fruits,
	'sauce': sauces
}

all_ingredients = [item for k in ingredients_list for item in ingredients_list[k]]

substitutes = {
	'allspice': 'half teaspoon cinnamon, quarter teaspoon ginger, and quarter teaspoon cloves per teaspoon of allspice',
	'arrowroot starch': 'cornstarch',
	'baking mix': 'pancake mix',
	'baking powder': 'quarter teaspoon baking soda plus half teaspoon cream of tartar per teaspoon of baking powder',
	'baking soda': '4 teaspoons of baking powder per teaspoon of baking soda',
	'beer': 'chicken broth',
	'brandy': 'imitation brandy extract and water',
	'beef broth': 'vegetable broth',
	'chicken broth': 'vegetable broth',
	'brown sugar': 'white sugar',
	'salted butter': 'margarine',
	'unsalted butter': 'vegetable oil',
	'butter': 'vegetable oil',
	'buttermilk': 'yogurt',
	'cheddar cheese': 'Monterey Jack cheese',
	'chervil': 'parsley',
	'chicken base': 'chicken broth',
	'chocolate': 'cocoa',
	'cocoa': 'chocolate',
	'condensed cream of mushroom soup': 'condensed cream of celery',
	'corn syrup': 'honey',
	'cottage cheese': 'ricotta cheese',
	'cracker crumbs': 'bread crumbs',
	'cream': 'milk and butter',
	'cream of tartar': 'lemon juice',
	'crème fraiche': 'Combine 1 cup of heavy cream and 1 tablespoon of plain yogurt. Let stand for 6 hours at room temperature',
	'egg': 'half a banana mashed with half teaspoon baking powder',
	'evaporated milk': 'light cream',
	"farmer's cheese": 'dry cottage cheese',
	'fats for baking': 'applesauce',
	'bread flour': '1 cup all-purpose flour plus 1 teaspoon wheat gluten per cup of bread flour',
	'cake flour': '1 cup all-purpose flour minus 2 tablespoons per cup of cake flour',
	'self-rising flour': 'seven-eighths cup all-purpose flour plus 1 and a half teaspoons baking powder and half teaspoon of salt per cup of self-rising flour',
	'garlic': 'garlic powder',
	'gelatin': 'agar agar',
	'ginger': 'ground ginger',
	'ground ginger': 'fresh ginger',
	'green onion': 'leek',
	'hazelnuts': 'almonds',
	'fresh herbs': 'dried herbs',
	'herring': 'sardines',
	'honey': 'corn syrup',
	'hot pepper sauce': 'three-fourths teaspoon cayenne pepper plus 1 teaspoon vinegar per teaspoon of hot pepper sauce',
	'lard': 'butter',
	'lemon grass': 'lemon zest',
	'lemon juice': 'lime juice',
	'lemon zest': 'lemon juice',
	'macadamia nuts': 'almonds',
	'mace': 'nutmeg',
	'margarine': 'butter',
	'mayonnaise': 'sour cream',
	'milk': 'soy milk or juice',
	'fresh mint': 'dried mint leaves',
	'molasses': 'Mix 3/4 cup brown sugar and 1 teaspoon cream of tartar per cup of molasses',
	'prepared mustard': 'Mix together 1 tablespoon dried mustard, 1 teaspoon water, 1 teaspoon vinegar and 1 teaspoon sugar per tablespoon of prepared mustard',
	'onion': 'leek',
	'orange juice': 'other citrus juice such as lemon juice',
	'orange zest': 'lemon juice',
	'parmesan cheese': 'Romano cheese',
	'parsley': 'chervil',
	'pepperoni': 'salami',
	'raisin': 'dried cranberries',
	'white rice': 'barley',
	'ricotta': 'silken tofu',
	'rum': 'half teaspoon rum extract, plus enough water to make 1 tablespoon per tablespoon of rum',
	'saffron': 'turmeric',
	'salami': 'pepperoni',
	'chocolate chips': 'chopped nuts',
	'shallots': 'onions',
	'shortening': 'butter',
	'sour cream': 'plain yogurt',
	'sour milk': '1 tablespoon vinegar or lemon juice mixed with enough milk to make 1 cup per cup of sour milk: Let stand 5 minutes to thicken',
	'soy sauce': 'quarter cup Worcestershire sauce mixed with 1 tablespoon water per half cup of soy sauce',
	'beef stock': '1 cube beef bouillon dissolved in 1 cup water per cup of beef stock',
	'chicken stock': '1 cube chicken bouillon dissolved in 1 cup water per cup of chicken stock',
	'sweetened condensed milk': '3/4 cup white sugar mixed with 1/2 cup water and 1 1/8 cups dry powdered milk per 14-ounce can of sweetened condensed milk: Bring to a boil and cook, stirring frequently, until thickened, about 20 minutes',
	'vegetable oil': 'apple sauce for baking and vegetable shortening for frying',
	'vinegar': 'lemon juice',
	'white sugar': 'honey',
	'wine': 'chicken broth',
	'yogurt': 'sour cream'
}


# -- INTENT TEMPLATES --

## Intent: START
start = [
	'I\'d like to start a recipe',
	'start',
	'start a recipe',
	'lets start a recipe',
	'begin recipe',
	'begin',
	'lets make something',
	'lets make a recipe'
	#Additions
	'I\'m ready'
]

# This intent is for showing information about the RECIPE, not the step
## Intent: SHOW
show = [
	'What are the ingredients',
	'show me the ingredients',
	'show ingredients',
	'whats this recipe called',
	'show me the recipe name',
	'show recipe name',
	'show recipe ingredients',
	'show recipe time',
]

## Intent: NAVIGATE
navigate = [
	'What is the next step',
	'Show me the next step',
	'whats next',
	'Show me the last step',
	'Show me the first step',
	'Show me the second step',
	'What is the fourth step',
	'What was the last step',
	'Repeat the last step',
	'Go backward',
	'Go forward',
	'What was before that',
	'What was the step before that',
	'What is after that',
	'What is the step after that',
	'Take me back',
	'Go back one step',
	'Go forward one step'
	'Go to the next step',
	'Tell me the next step',
	'Tell me the previous step',
	'Next step',
	'Previous step',
	'Last step',
	'Next',
	'I\'m done with this step',
	'Take me to the last step',
	'I finished',
]

## Intent: SEARCH
search = [
	'How do I (action) something',
	'How do I (action) something with a (tool)',
	'What is (food)',
	'What is (tool)',
	'How can I (action) (food)',
	#Additions
	'How do I (action)',
	'How do I (action) with a (tool)',
	'What is a (food)',
	'What is a (tool)',

]

# This intent is for showing information about the STEP not the recipe
## Intent: GET_PARAM
get_param = [
	'how long does (food) cook',
	'how long do I put it in for',
	'for how long',
	'how long does that take',
	'what is the temperature',
	'what temperature',
	'what temperature does (food) cook',
	'When is it done',
	'How much (food) do I need',
	'How much (food)',
	#Additions
	'How long do I (action)'
	'How long does (action) take'
]

## Intent: SUBSTITUTE
substitute = [
	'What can I susbtitute for (food)',
	'What is a good replacement for (food)',
	'What can I use instead of (food)',
	'replace (food)',
	'substitute (food)',
	'How can I substitute (food)'
]

## Intent: UKNOWN
unknown = [
	'(food) (food)',
	'     ',
	'(tool) (tool)',
	'(action) (action)',
]

## Intent: ACKNOWLEDGE
acknowledge = [
	'Okay',
	'Yes',
	'Fine',
	'Sure',
	'I Understand',
	'Alright'
	'All right'
	'okey-dokey'
	'roger'
	'uh-huh'
	'Ok',
	'Thanks',
	'Thank you'
]
