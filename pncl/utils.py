import numpy as np

COLORS = [
    (75, 192, 192),   # Light blue
    (240, 139, 75),   # Orange
    (75, 192, 75),    # Green
    (192, 75, 75),    # Red
    (75, 75, 192),    # Blue
    (192, 192, 192),  # Light gray
    (192, 75, 192),   # Pink
    (192, 192, 75),   # Yellow
    (75, 75, 75),     # Dark gray
]


def _color_generator():
    i = 0
    while True:
        yield COLORS[i]
        i += 1
        if i == len(COLORS):
            i = 0


class Color:
    gen = _color_generator()

    @staticmethod
    def next():
        return Color.gen.__next__()

    @staticmethod
    def get(i):
        return COLORS[i % len(COLORS)]


def check_args(*args):
    output = list(args)
    for i in range(len(output)):
        if isinstance(output[i], list):
            pass
        elif isinstance(output[i], np.ndarray):
            output[i] = output[i].tolist()
        else:
            raise TypeError('Data must be either a list or a rank 1 np.ndarray.')

    return output


def lists_to_points(x, y):
    output = [{'x': x[i], 'y': y[i]} for i in range(len(x))]
    return output
