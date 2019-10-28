from copy import deepcopy

from pncl.utils import check_args, Color, lists_to_points


class Plot:
    def __init__(self, *args, **kwargs):
        self.type = None
        self.x = None
        self.y = None
        self.datasets_labels = None
        self.x_label = None
        self.y_label = None

    def get_datasets(self):
        pass

    def get_x_labels(self):
        pass

    def get_datasets_labels(self):
        if self.datasets_labels is None:
            self.datasets_labels = ['Data {}'.format(i) for i in range(len(self.y))]
        return self.datasets_labels

    def get_options(self):
        options = {
            'maintainAspectRatio': False,
            'elements': {
                'point': {
                    'radius': 0,
                    'borderWidth': 1
                },
                'line': {
                    'tension': 0.1,
                    'borderWidth': 1,
                    'fill': False
                },
                'rectangle': {
                    'borderWidth': 1
                },
                'arc': {
                    'borderWidth': 1
                }
            },
            'scales': {
                'xAxes': [{
                    'scaleLabel': {
                        'display': self.x_label is not None,
                        'labelString': self.x_label
                    }
                }],
                'yAxes': [{
                    'scaleLabel': {
                        'display': self.y_label is not None,
                        'labelString': self.y_label
                    }
                }]
            },
            'animation': {
                'duration': 500
            }
        }
        return options

    def get_style(self, subplot):
        color = Color.get(subplot)
        return {
            'borderColor': 'rgba({}, {}, {}, 1)'.format(*color),
            'backgroundColor': 'rgba({}, {}, {}, 0.2)'.format(*color),
        }

    def refresh(self, *args, **kwargs):
        self.datasets_labels = kwargs.get('labels', None)
        self.x_label = kwargs.get('x_label', None)
        self.y_label = kwargs.get('y_label', None)

        args = deepcopy(args)
        args = check_args(*args)
        if len(args) == 1:
            # Only one y
            self.x = list(range(len(args[0])))
            self.y = args
        else:
            # One x and at least one y
            self.x = args[0]
            self.y = args[1:]

    def push(self, *args):
        if len(args) == 1:
            if len(self.y) > 1:
                raise ValueError(
                    'add() requires a value for x and a value for each line, '
                    'or a single value if there is only one line.'
                )
            # Only one y
            self.x.append(self.x[-1] + 1)
            self.y[0].append(args[0])
        else:
            if len(args) != len(self.y) + 1:
                raise ValueError(
                    'add() requires a value for x and a value for each line, '
                    'or a single value if there is only one line.'
                )
            # One x and at least one y
            self.x.append(args[0])
            for i in range(len(self.y)):
                self.y[i].append(args[i + 1])

    def last_pushed(self):
        output = {
            'label': None,
            'datasets': None
        }
        labels = self.get_x_labels()
        if labels:
            output['label'] = labels[-1]

        datasets = self.get_datasets()
        datasets = [
            {key: value[-1] for key, value in d.items() if isinstance(value, list)}
            for d in datasets
        ]
        output['datasets'] = datasets

        return output

    def to_dict(self):
        pass


class Line(Plot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh(*args, **kwargs)

        self.type = 'line'

    def get_datasets(self):
        datasets = []
        datasets_labels = self.get_datasets_labels()
        for i, y in enumerate(self.y):
            dataset = {
                'label': datasets_labels[i],
                'data': lists_to_points(self.x, y)
            }
            dataset.update(self.get_style(i))
            datasets.append(dataset)

        return datasets

    def get_x_labels(self):
        return None

    def get_options(self):
        options = super().get_options()
        options['scales']['xAxes'][0]['type'] = 'linear'
        return options

    def to_dict(self):
        plot = {
            'type': self.type,
            'data': {
                'labels': self.get_x_labels(),
                'datasets': self.get_datasets()
            },
            'options': self.get_options()
        }
        return plot


class Bar(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = 'bar'
        self.has_labels = True

    def get_x_labels(self):
        return self.x

    def get_options(self):
        options = super().get_options()
        options['scales']['xAxes'][0]['type'] = 'category'
        return options


class Radar(Bar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = 'radar'

    def get_datasets(self):
        datasets = []
        datasets_labels = self.get_datasets_labels()
        for i, y in enumerate(self.y):
            dataset = {
                'label': datasets_labels[i],
                'data': y,
            }
            dataset.update(self.get_style(i))
            datasets.append(dataset)

        return datasets

    def get_options(self):
        options = super().get_options()
        options['scales'] = None
        options['elements']['line']['fill'] = True
        return options


class Pie(Plot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh(*args, **kwargs)

        self.type = 'pie'

    def get_datasets(self):
        datasets = []
        for i, y in enumerate(self.y):
            dataset = {
                'data': y,
            }
            dataset.update(self.get_style(i))
            datasets.append(dataset)

        return datasets

    def get_options(self):
        options = super().get_options()
        options['scales'] = None
        return options

    def get_x_labels(self):
        return self.x

    def get_style(self, subplot):
        colors = [Color.get(i) for i in range(len(self.x))]
        return {
            'borderColor': ['rgba({}, {}, {}, 1)'.format(*c) for c in colors],
            'backgroundColor': ['rgba({}, {}, {}, 0.2)'.format(*c) for c in colors]
        }

    def to_dict(self):
        plot = {
            'type': self.type,
            'data': {
                'labels': self.get_x_labels(),
                'datasets': self.get_datasets()
            },
            'options': self.get_options()
        }
        return plot


class Doughnut(Pie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = 'doughnut'


class PolarArea(Pie):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = 'polarArea'


class Scatter(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = 'scatter'

    def get_options(self):
        options = super().get_options()
        options['elements']['point']['radius'] = 2
