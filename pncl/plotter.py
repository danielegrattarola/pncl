import atexit
import json
import multiprocessing
import webbrowser
from math import ceil

from pncl.plots import Line, Bar, Pie, Scatter, Radar, Doughnut, PolarArea
from pncl.server import Server


class Pencil:
    def __init__(self, grid=2, col_height=300, sticky=True, host='0.0.0.0',
                 port=8080, events_per_second=1):
        """
        This is the main class of the package, and the only one you'll be using.
        Arguments:
        - `grid` (default: `2`): structure of the grid. If integer, the grid
        will be equally divided in that many columns and updated dynamically.
        If list of integers, the grid will be fixed and for each element in the
        list there will be a row with that many columns.
        - `col_height` (default: `300`): height of the rows, in pixels.
        - `sticky` (default: `True`): if `True`, Pencil will keep the server alive
        when the main script terminates. You will have to kill the program
        manually using `Ctrl + C`. If `False`, Pencil will be shut down
        automatically and you will lose your plots if you did not have the web
        page open in a browser (or if you refresh the page after the script
        terminates).
        - `host` (default: `'0.0.0.0'`): IP address for hosting the web server.
        Do not change it if you don't know what you are doing. This is the host
        for the `aiohttp` instance that serves the content.
        - `port` (default: `8080`): port on which the server listens.
        - `events_per_second` (default: `1`): how many times per second should
        the content be refreshed. Setting a high value may cause performance
        issues.
        """
        self._event_manager = multiprocessing.Manager()
        self._event_queue = self._event_manager.Queue()
        self._config_queue = self._event_manager.Queue()
        self.global_lock = self._event_manager.Lock()
        self._server = Server(host=host, port=port, events_per_second=events_per_second)
        self._server.start(self._event_queue, self._config_queue)
        self.sticky = sticky
        if not self.sticky:
            atexit.register(self.stop)
        else:
            atexit.register(self._event_queue.join)

        self.grid = grid
        self.plots = []
        self._config = {
            'grid': grid if grid else [],
            'height': int(col_height),
            'plots': []
        }
        
    def line(self, *args, **kwargs):
        """
        Adds a line plot to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        - `x_label`: string, the custom label for the x-axis.
        - `y_label`: string, the custom label for the y-axis.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = Line(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()

    def bar(self, *args, **kwargs):
        """
        Adds a bar plot to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        `x` can also assume categorical values (e.g., list of strings) and will
        be displayed accordingly.
        - `x_label`: string, the custom label for the x-axis.
        - `y_label`: string, the custom label for the y-axis.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = Bar(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()

    def radar(self, *args, **kwargs):
        """
        Adds a radar plot to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        `x` can also assume categorical values (e.g., list of strings) and will
        be displayed accordingly.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = Radar(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()

    def pie(self, *args, **kwargs):
        """
        Adds a pie chart to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        `x` can also assume categorical values (e.g., list of strings) and will
        be displayed accordingly.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = Pie(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()

    def doughnut(self, *args, **kwargs):
        """
        Adds a doughnut plot to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        `x` can also assume categorical values (e.g., list of strings) and will
        be displayed accordingly.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = Doughnut(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()

    def polar_area(self, *args, **kwargs):
        """
        Adds a polar area chart to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        `x` can also assume categorical values (e.g., list of strings) and will
        be displayed accordingly.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = PolarArea(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()

    def scatter(self, *args, **kwargs):
        """
        Adds a scatter plot to the grid.
        Arguments:
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword
        arguments. All lists after `x` are optional. If they are passed, they
        will be used as independent data sets and plotted vs. `x`. If only `x`
        is given, it will be plotted as a data set itself, vs. an integer
        sequence `range(len(x))`.
        - `x_label`: string, the custom label for the x-axis.
        - `y_label`: string, the custom label for the y-axis.
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        plot = Scatter(*args, **kwargs)
        self.plots.append(plot)
        self._config['plots'].append(plot.to_dict())
        self._new_grid()
        
    def refresh(self, plot_idx, *args, **kwargs):
        """
        Updates the indicated plot with new data.
        Arguments:
        - `index`: integer, zero-based index to select the plot to refresh (in
        order of creation).
        - `x, y1, ..., yn`: 1D lists or Numpy arrays, passed as non-keyword arguments.
        - `x_label`: string, the custom label for the x-axis (only has effect
        on `line`, `bar`, and `scatter` plots).
        - `y_label`: string, the custom label for the y-axis (only has effect
        on `line`, `bar`, and `scatter` plots).
        - `labels`: list of strings, one for each `y1, ..., yn`. The custom
        labels for the legend.
        """
        self.plots[plot_idx].refresh(*args, **kwargs)
        self._config['plots'][plot_idx] = self.plots[plot_idx].to_dict()
        event = {
            'type': 'refresh',
            'idx': plot_idx,
            'data': self._config['plots'][plot_idx],
        }
        event = json.dumps(event)
        self._event_queue.put(event)
        self._update_config()

    def push(self, plot_idx, *args):
        """
        Appends a new data point to a plot. If more than one data set was passed
        when creating the plot, appends a data point to each data set.
        Arguments:
        - `index`: integer, zero-based index to select the plot to refresh (in
        order of creation).
        - `x, y1, ..., yn`: scalar numbers, passed as non-keyword arguments. You
        must pass a scalar for each data set in the plot.

        """
        self.plots[plot_idx].push(*args)
        self._config['plots'][plot_idx] = self.plots[plot_idx].to_dict()
        event = {
            'type': 'push',
            'idx': plot_idx,
            'data': self.plots[plot_idx].last_pushed()
        }
        event = json.dumps(event)
        self._event_queue.put(event)
        self._update_config()

    def set_grid(self, grid=2):
        """
        Re-arranges the grid with the given configuration.
        Arguments:
        - `grid` (default: `2`): integer or list of integers. If integer, the
        grid will be equally divided in that many columns and updated
        dynamically. If list of integers, the grid will be fixed and for each
        element in the list there will be a row with that many columns (make
        sure that the numbers in the list sum up to at least the number of
        plots).
        """
        self.grid = grid
        self._new_grid()

    def browser(self):
        """
        Opens a new tab in the default browser at `host:port` as specified when
        creating the `Pencil` instance (default `0.0.0.0:8080`).
        """
        webbrowser.open(self._server.get_endpoint(), new=0, autoraise=True)

    def stop(self):
        """
        Kills the Pencil backend server. After stopping Pencil, all plots will be lost
        if you close or refresh the page. This method is called automatically at
        the end of your script if setting `sticky=False` when creating the `Pencil`
        instance.
        """
        self._server.stop()

    def _new_grid(self):
        self._check_grid()
        event = {
            'type': 'new_grid',
            'data': self._config
        }
        event = json.dumps(event)
        self._event_queue.put(event)
        self._update_config()

    def _check_grid(self):
        n_plots = len(self._config['plots'])

        if isinstance(self.grid, list):
            if sum(self.grid) < n_plots:
                raise ValueError(
                    'Too many plots ({}) for grid ({})'.format(n_plots, self._config['grid'])
                )
            self._config['grid'] = self.grid
        else:
            self._config['grid'] = [
                self.grid for _ in range(ceil(n_plots / self.grid))
            ]

    def _update_config(self):
        # Empty the queue
        while True:
            try:
                self._config_queue.get(block=False)
            except:
                break
        self._config_queue.put(json.dumps(self._config))
