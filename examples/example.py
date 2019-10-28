import numpy as np

from pncl import Pencil

# Create the main Pencil instance
p = Pencil(grid=[2, 4, 1], sticky=True)

# Open the web page in the browser
p.browser()

# Create some plots
input('Press Enter to create plots')
x = np.arange(10)
x_cat = ["Cats", "Dogs", "Birds", "Llamas"]
p.line(x, x ** 2, labels=['Line'])
p.bar(x, np.cos(x), labels=['Bar'])
p.radar(x, x + 3, labels=['Radar'])
p.pie(x_cat, [2, 3, 4, 5])
p.doughnut(x_cat, [2, 3, 4, 5])
p.polar_area(x_cat, [2, 3, 4, 5])
p.scatter(x, np.random.rand(x.shape[0]), labels=['Scatter'])

# Wait three seconds and then add some new data to the plots
input('Press Enter to push new data')
x = 10
p.push(0, x, x ** 2)
p.push(1, x, np.cos(x))
p.push(2, x, x + 3)
p.push(3, "Aardvarks", 6)
p.push(4, "Aardvarks", 6)
p.push(5, "Aardvarks", 6)
p.push(6, x, np.random.random())

# Refresh the plots with some new data
input('Press Enter to refresh plots')
p.refresh(0, np.arange(10), np.random.rand(10), np.random.rand(10))
p.refresh(1, np.arange(10), np.random.rand(10))
p.refresh(2, np.arange(10), np.random.rand(10))
p.refresh(3, ["Cats", "Dogs", "Birds", "Llamas"], np.random.randint(2, 9, size=4))
p.refresh(4, ["Cats", "Dogs", "Birds", "Llamas"], np.random.randint(2, 9, size=4))
p.refresh(5, ["Cats", "Dogs", "Birds", "Llamas"], np.random.randint(2, 9, size=4))
p.refresh(6, np.arange(10), np.random.rand(10))

# Wait three seconds and then change the grid
input('Press Enter to change grid')
p.set_grid([2, 3, 2])
