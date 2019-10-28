---
title: Pencil
layout: default
---
## Welcome to Pencil  <i class="fas fa-pencil-alt"></i>

Pencil is a small Python library to create plots in the browser using [Charts.js](https://chartjs.org).

Pencil makes it easy to draw your charts in a dynamic and responsive grid, and lets you update your plots live as the data is created. 

With Pencil, you can draw seven different types of charts: 

- Line
- Bar
- Radar
- Pie
- Doughnut
- Polar area
- Scatter

<ul class="topnav">
    <li><a class="rounded" href="https://github.com/danielegrattarola/pncl"><i class="fab fa-github"></i> GitHub</a></li>
</ul>

---

## Table of contents

- [Installation](#installation)
- [Usage](#usage)
  * [Creating charts](#creating-charts)
  * [Refreshing charts](#refreshing-charts)
  * [Adding new points](#adding-new-points)
  * [Chart labels](#chart-labels)
  * [Changing the grid](#changing-the-grid)
  * [Saving plots](#saving-plots)
- [Arguments](#arguments)
  * [<code>Pencil()</code>](#pencil)
  * [<code>Pencil.line() | bar() | radar() | pie() | doughnut() | polar_area() | scatter()</code>](#pencilline--bar--radar--pie--doughnut--polar_area--scatter)
  * [<code>Pencil.refresh()</code>](#pencilrefresh)
  * [<code>Pencil.push()</code>](#pencilpush)
  * [<code>Pencil.set_grid()</code>](#pencilset_grid)
  * [<code>Pencil.browser()</code>](#pencilbrowser)
  * [<code>Pencil.stop()</code>](#pencilstop)
- [Contributing](#contributing)

---

## Installation

Pencil is available on the Python Package Index and can be installed with `pip`:

```sh
$ pip install pncl
```

If you want, you can also install the package from source with:

```sh
$ git clone https://github.com/danielegrattarola/pncl.git
$ cd pncl
$ pip install .
```

Pencil requires Python 3.6.5+, and works on Linux and MacOS.

---

## Usage

To start making plots, you simply need to create a `Pencil` instance and open a browser window:

```python
from pncl import Pencil

p = Pencil()
p.browser()  # Open the default browser on 0.0.0.0:8384
```

By default, plots will be arranged in a grid with two columns and added automatically left-to-right, top-to-bottom. A new row will be created automatically every two plots. 
To change the number of columns, you can set the `grid` argument as follows:

```python
p = Pencil(grid=1)  # One plot per row
```

If you want, you can also define a fixed grid by passing a list of integers, where each element indicates the number of columns in each row:

```python
p = Pencil(grid=[2, 1, 2])
```

### Creating charts
To create charts, you simply call one of the seven methods exposed by `Pencil`:

- `p.line(...)`
- `p.bar(...)`
- `p.radar(...)`
- `p.pie(...)`
- `p.doughnut(...)`
- `p.polar_area(...)`
- `p.scatter(...)`

For instance, to create a simple line chart you can call:

```python 
y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
p.line(y)
```

If you want to specify the values on the x-axis, simply pass them as first argument:

```python
x = [0, 2, 4, 6, 8, 10]
y = [1, 1, 2, 3, 5, 8]
p.line(x, y)
```

If you want to plot more than one series of data on the same chart, you can pass as many arrays as you want after `x`:

```python
x = np.arange(10). # Pencil works just fine with Numpy arrays
p.line(x, np.sin(x), np.cos(x))
```

All charts in Pencil work in the same way, you just need to call the corresponding functions. Try these out:

```python
# Bar chart
p.bar(np.arange(10), np.random.randn(10))

# Radar chart
p.radar(np.arange(10), np.random.randn(10))

# Pie chart
p.pie(["Cats", "Birds", "Llamas"], np.random.randint(10, size=3))

# Doughnut chart
p.doughnut(["Cats", "Birds", "Llamas"], np.random.randint(10, size=3))

# Polar area chart
p.polar_area(["Cats", "Birds", "Llamas"], np.random.randint(10, size=3))

# Scatter chart
p.scatter(np.arange(10), np.random.rand(10))
```

### Refreshing charts

Pencil keeps track of your plots by assigning them a sequential integer index starting from 0.
If you want to change the data shown in one plot, you can use the `refresh` method:

```python
# Create a plot
x = np.arange(10)
p.line(x, np.sin(x))

# Changed your mind?
p.refresh(0, x, np.cos(x))
```

You can also use this method to add new data series to your plots:

```python
# Create a plot
x = np.arange(10)
p.line(x, np.sin(x))

# Add a new series
p.refresh(0, x, np.sin(x), np.cos(x))
```

### Adding new points

Sometimes, it can be useful to update a plot live as new points are created by your program.
In this case, you can `push` new samples as follows:

```python
# Create a plot with two data series
x = np.arange(10)
p.line(x, np.sin(x), np.cos(x))

# Add new data
for i in range(11, 20):
    p.push(0, i, np.sin(i), np.cos(i))
```

The `push` method only takes scalars, not arrays. If you want to add entire arrays to your plots, it's better to `refresh` them.

### Chart labels

When creating a plot, you can pass the `labels` keyword argument to specify custom labels to use in the legend. This should be a list of strings, one for each `y` series that you are plotting. 

When creating line, bar, or scatter plots, you can also specify labels for the axes with:
- `x_label`: label for the x-axis.
- `y_label`: label for the y-axis. 

For example:

```python
x = np.arange(10)

# Plot with custom legend
p.line(x, np.sin(x), np.cos(x), labels=['Happiness', 'Cookies'])

# Plot with custom axis labels
p.line(x, np.exp(x), x_label='Time', y_label='Swag')
```

Note that the same keyword arguments can also be passed to `refresh` when changing an existing plot.

### Changing the grid

You can change how plots are arranged by calling `set_grid`:

```python
# Divide all rows equally into 3 columns
p.set_grid(3)

# Define a new custom grid 
p.set_grid([1, 2, 3])
```

### Saving plots

To save a plot, simply click on it from the browser window. It will be downloaded automatically. 

---

## Arguments

### `Pencil()`

This is the main class of the package, and the only one you'll be using. It takes the following arguments:

- `grid` (default: `2`): structure of the grid. If integer, the grid will be equally divided in that many columns and updated dynamically. If list of integers, the grid will be fixed and for each element in the list there will be a row with that many columns.
- `col_height` (default: `300`): height of the rows, in pixels.
- `sticky` (default: `True`): if `True`, Pencil will keep the server alive when the main script terminates. You will have to kill the program manually using `Ctrl + C`. If `False`, Pencil will be shut down automatically and you will lose your plots if you did not have the web page open in a browser (or if you refresh the page after the script terminates).    
- `host` (default: `'0.0.0.0'`): IP address for hosting the web server. Do not change it if you don't know what you are doing. This is the host for the `aiohttp` instance that serves the content.
- `port` (default: `8080`): port on which the server listens. 
- `events_per_second` (default: `1`): how many times per second should the content be refreshed. Setting a high value may cause performance issues.

### `Pencil.line() | bar() | radar() | pie() | doughnut() | polar_area() | scatter()`

Adds a plot of the corresponding type to the grid. All methods have the same signature:

- `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword arguments. All lists after `x` are optional. If they are passed, they will be used as independent data sets and plotted vs. `x`. If only `x` is given, it will be plotted as a data set itself, vs. an integer sequence `range(len(x))`.  
When calling `bar()`, `radar()`, `pie()`, `doughnut()`, and `polar_area()`, `x` can also assume categorical values (e.g., list of strings) and will be displayed accordingly.
- `x_label`: string, the custom label for the x-axis (only has effect on `line`, `bar`, and `scatter`).
- `y_label`: string, the custom label for the y-axis (only has effect on `line`, `bar`, and `scatter`).
- `labels`: list of strings, one for each `y1, ..., yn`. The custom labels for the legend. 

### `Pencil.refresh()`

Updates the indicated plot with new data. Its signature is the same as the methods for creating plots, except that the first argument must be an integer indicating which plot to refresh:

- `index`: integer, zero-based index to select the plot to refresh (in order of creation).
- `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword arguments.
- `x_label`: string, the custom label for the x-axis (only has effect on `line`, `bar`, and `scatter`).
- `y_label`: string, the custom label for the y-axis (only has effect on `line`, `bar`, and `scatter`).
- `labels`: list of strings, one for each `y1, ..., yn`. The custom labels for the legend. 

### `Pencil.push()`

Appends a new data point to a plot. If more than one data set was passed when creating the plot, appends a data point to each data set. 

- `index`: integer, zero-based index to select the plot to refresh (in order of creation).
- `x, y1, ..., yn`: scalar numbers, passed as non-keyword arguments. You must pass a scalar for each data set in the plot.

### `Pencil.set_grid()`

Re-arranges the grid with the given configuration:

- `grid` (default: `2`): integer or list of integers. If integer, the grid will be equally divided in that many columns and updated dynamically. If list of integers, the grid will be fixed and for each element in the list there will be a row with that many columns (make sure that the numbers in the list sum up to at least the number of plots).

### `Pencil.browser()`

Opens a new tab in the default browser at `host:port` as specified when creating the `Pencil` instance (default `0.0.0.0:8080`).

### `Pencil.stop()`

Kills the Pencil backend server. After stopping Pencil, all plots will be lost if you close or refresh the page. This method is called automatically at the end of your script if setting `sticky=False` when creating the `Pencil` instance.

---

## Contributing

If you find any issues with the package or if you want to add a new functionality to Pencil, you can pop over at [Github](https://github.com/danielegrattarola/pncl).

