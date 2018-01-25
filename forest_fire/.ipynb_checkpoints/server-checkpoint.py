from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from forest_fire.model import ForestFire



def forest_fire_portrayal(tree):
    
    if tree.type is "Bird":
        portrayal = {"Shape": "circle", "r": 0.7, "Filled": "true", "Layer": 2}
        (x, y) = tree.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        colors = {
            5: "#394EDB",
            4: "#6E35CD",
            3: "#8417E1",
            2: "#A60FDC",
            1: "#D50DE8",
            0: "#FA03C3",
        }
        portrayal["Color"] = colors[tree.hunger]
        return portrayal

    elif tree.type is "Tree":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 1}
        (x, y) = tree.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        colors = {"Fine": "#00AA00",
                  "On Fire": "#880000",
                  "Burned Out": "#413B3B",
                 }
        portrayal["Color"] = colors[tree.condition]
        return portrayal

    else:# tree.type is "Empty":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        (x, y) = tree.get_pos()
        portrayal["x"] = x
        portrayal["y"] = y
        colors = {
            "Nothing": "#000000",
        }
        portrayal["Color"] = [tree.condition]
        #return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 800, 800)
#tree_chart = ChartModule([{"Label": "Fine", "Color": "green"},
#                          {"Label": "On Fire", "Color": "red"},
#                          {"Label": "Burned Out", "Color": "black"}])

h_slider = UserSettableParameter('slider', "Height", 100, 1, 100, 1)
w_slider = UserSettableParameter('slider', "Width", 100, 1, 100, 1)
d_slider = UserSettableParameter('slider', "Density", 0.65, 0.01, 1, 0.01)
c_slider = UserSettableParameter('slider', "Catch Chance - Setup Only", 0.5, 0, 1, 0.01)
b_slider = UserSettableParameter('slider', "Burnout Chance - Setup Only", 0.5, 0, 1, 0.01)
bd_slider = UserSettableParameter('slider', "Bird Density - Setup Only", 0.1, 0, 1, 0.01)


server = ModularServer(ForestFire, 
                       [canvas_element],
                       "Forest Fire", 
                       model_params = {'height': w_slider,
                                       'width': h_slider,
                                       'density': d_slider,
                                       'catch_chance': c_slider,
                                       'burnout_chance': b_slider,
                                       'bird_density': bd_slider,
                                      })
#, tree_chart