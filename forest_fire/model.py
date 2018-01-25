import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from forest_fire.agent import TreeCell, Bird, Empty


class ForestFire(Model):
    """
    Simple Forest Fire model.
    """
    def __init__(self, height, width, density, catch_chance, burnout_chance):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density
        self.catch_chance = catch_chance
        self.burnout_chance = burnout_chance

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {"Fine": lambda m: self.count_type(m, "Fine"),
             "On Fire": lambda m: self.count_type(m, "On Fire"),
             "Burned Out": lambda m: self.count_type(m, "Burned Out")})

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if random.random() < self.density:
                # Create a tree
                new_tree = TreeCell((x, y), self, self.catch_chance, self.burnout_chance)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        
        for (contents, x, y) in self.grid.coord_iter():
            if random.random() < (self.density * 0.1):
                new_bird = Bird((x, y), self)
                self.grid._place_agent((x, y), new_bird)
                self.schedule.add(new_bird)
                
        for (contents, x, y) in self.grid.coord_iter():
            new_empty = Empty((x, y), self)
            self.grid._place_agent((x, y), new_empty)
            self.schedule.add(new_empty)
                
        self.running = True
        
        # Place a bird in every 10th tree

                

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
