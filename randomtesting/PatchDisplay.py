from bokeh.io import output_notebook, show
from bokeh.plotting import figure

def displayPatch(patch):
    graph = figure(width=600, height=600)
    
    graph.circle(patch[0], patch[1], size=patch[2], line_color = "Navy", fill_color = patch[3], fill_alpha = 0.3)

    show(graph)

