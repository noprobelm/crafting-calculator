import sys

sys.path.insert(0,"..")
from calculator import CraftCalc

# The directory of the csv file containing the recipe table data.
csv = "../data/csv/satisfactory.csv"

# A list of the ingredient columns from the csv
icols = ["Ingredient 1", "Ingredient 2", "Ingredient 3", "Ingredient 4"]

# A list of the ingredient input columns (for satisfactory, the data
# in these columns represent the number of ingredients required to
# produce 1 of a recipe per minute.)
i_input_cols = ["Ingredient 1 Rate", "Ingredient 2 Rate",
                  "Ingredient 3 Rate", "Ingredient 4 Rate"]

# Additional arbitrary attributes to be associated with each recipe
# to be used in future methods of the CraftCalc class.
recipe_attrs = {"building" : "Building",
                "output_rate" : "Building Output Rate",
                "alternate" : "Alternate",
                "alternate_of" : "Alternate of"}

# Creates a CraftCalc object based on the Satisfactory recipes csv.
sat = CraftCalc.Calculator(csv=csv, rcol="Recipe", icols=icols,
                           i_input_cols=i_input_cols, recipe_attrs=recipe_attrs)


# Prompts the user for recipe input
recipe = input("Input a recipe: ")

# Prompts the user for the number of desired recipe to output
num_output = float(input("Input the number of recipe desired for production (default=1): "))
if num_output == None:
    num_output = float(1)

# Calls the CraftCalc.calc_recipe() function and returns a dict of the
# ingredients and the required number for each.
ingredients = sat.calc_recipe(recipe, num_output)
print(f"Ingredients required to produce {num_output} unit(s) of {recipe}:\n{ingredients}")
