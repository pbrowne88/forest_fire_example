from mesa import Agent
import random


class Empty(Agent):
    
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.type = "Empty"
        self.condition = "Nothing"
        self.hunger = 0
        
    def step(self):
        self.hunger = 0
        
    def get_pos(self):
        return self.pos

class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """
    def __init__(self, pos, model, catch_chance, burnout_chance):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.catch_chance = catch_chance
        self.burnout_chance = burnout_chance
        self.type = "Tree"

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    if random.random() < self.catch_chance:
                        neighbor.condition = "On Fire"
            if random.random() < self.burnout_chance:
                self.condition = "Burned Out"

    def get_pos(self):
        return self.pos
    
    
class Bird(Agent):
    """
    A hungry bird.
    """
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Not Carrying Fire"
        self.hunger = 5
        self.type = "Bird"
        
    def step(self):
        #Digest
        if self.hunger > 0:
            self.hunger -= 1
        #Move  
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
        #Search for Prey
        if self.hunger == 0:
            for neighbor in self.model.grid.neighbor_iter(self.pos):    
                if neighbor.condition == "Fine" and self.condition == "Carrying Fire":
                    neighbor.condition = "On Fire"
                    self.condition = "Not Carrying Fire"
                    self.hunger = 5
                if neighbor.condition == "On Fire" and self.condition == "Not Carrying Fire" and self.hunger == 0:
                    self.condition = "Carrying Fire"
                    
    def get_pos(self):
        return self.pos
                
            
        
                

                
                
            
        
        