import pandas as pd
import numpy as np
import networkx as nx

class Calculator:
    """Class for a generic crafting calculator.

    A Calculator object stores a csv recipe table as a Pandas
    DataFrame and a directed graph structure (networkx DiGraph).

    The methods within use the DiGraph to retrieve information about
    a recipe and/or perform operations to assist in planning.

    Parameters
    ----------
    csv : csv
        A csv must be a csv-readable file with rows representing
        information about a unique recipe, such as the ingredients
        required to produce it. csv headers defining each column
        are required.
    rcol: Recipe column
        String defining the name of the recipe column from the csv
    icols : Ingredient columns
        Dict defining the ingredient columns in the csv for each recipe.
        Keys should be the columns containing the ingredient names; values
        are the number for each required to produce a single unit of the
        recipe.
    i_input_cols : Ingredient input columns
        List defining the columns containing information on the number
        of ingredients required to produce one of a recipe.
    recipe_attrs : Recipe Attributes (optional, default: None)
        Dict whose key is the attribute to be used when referencing
        additional information about a recipe, (e.g. prerequisite skill,
        object, or other information to be used in a calculation.) and
        whose value is the column name to be referenced from the csv.

    """

    def __init__(self, csv, rcol, icols, recipe_attrs=None):
        self.df = pd.read_csv(csv).set_index(rcol)
        self.G = self.build_graph(icols, recipe_attrs)
        self.recipes = list(self.G.nodes)

    def build_graph(self, icols, recipe_attrs):
        """Generates the DiGraph structure to be used when calculating
        recipe requirements.
        """
        df = self.df
        def add_nodes():
            G.add_nodes_from(df.index)
            for n in df.index:
                for ingredient, num_input in zip(tuple(df[df.index == n][icols.keys()].dropna(axis=1).values[0]),
                                                tuple(df[df.index == n][icols.values()].dropna(axis=1).values[0])):
                    G.add_edge(n, ingredient, num_input=num_input)

        def add_recipe_attrs():
            if recipe_attrs:
                for attr in recipe_attrs:
                    for n in df.index:
                        G.nodes[n][attr] = df[df.index == n][recipe_attrs[attr]].values[0]

        G = nx.DiGraph()
        add_nodes()
        add_recipe_attrs()
        return G

    def calc_recipe(self, recipe, num_output=1):
        """Returns a dict of the total number of components required
        to produce a recipe all the way down to the raw materials,
        irrespective of where the materials should be allocated to
        throughout the graph.

        Parameters:
        --------
        recipe: Recipe
            String representing the recipe desired for production
        num_output: num output (optional, default: 1)
            The number of recipe desired for production.

        """
        p = nx.predecessor(self.G, recipe)
        sg = nx.subgraph(self.G, p).copy()
        ingredients = dict(zip([n for n in sg.nodes], [0 for n in range(len(sg.nodes))]))
        ingredients[recipe] = num_output
        for ing in ingredients:
            paths = [path for path in nx.all_simple_edge_paths(sg, recipe, ing)]
            for path in paths:
                product = num_output
                for u, v in path:
                    product = product * sg.edges[u, v]["num_input"]
                ingredients[ing] += product
        return ingredients
