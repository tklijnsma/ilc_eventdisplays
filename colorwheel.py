import numpy as np

class ColorWheel:
    '''Returns a consistent color when given the same object'''
    def __init__(self, colors=None, seed=44, assignments=None, shuffle=True, n=None):
        if colors is None:
            import matplotlib._color_data as mcd
            self.colors = list(mcd.XKCD_COLORS.values())
        # elif colors == 'viridis':
        #     from matplotlib import cm
        #     from colour import Color
        #     if n is None: n = 30
        #     viridis = cm.get_cmap('viridis', n)
        #     self.colors = [ Color(rgb=viridis(i/float(n))[:-1]).hex for i in range(n) ]
        else:
            self.colors = colors
        if shuffle:
            np.random.seed(seed)
            np.random.shuffle(self.colors)
        self._original_colors = self.colors.copy()
        self.assigned_colors = {}
        if assignments:
            [self.assign(k, v) for k, v in assignments.items()]
        
    def make_key(self, thing):
        try:
            return int(thing)
        except ValueError:
            return thing

    def __contains__(self, thing):
        return self.make_key(thing) in self.assigned_colors

    def __call__(self, thing):
        key = self.make_key(thing)
        if key in self.assigned_colors:
            # print(f'Returning pre-assigned color: {key}:{self.assigned_colors[key]}')
            return self.assigned_colors[key]
        else:
            color = self.colors.pop()
            self.assigned_colors[key] = color
            if not(self.colors): self.colors = self._original_colors.copy()
            # print(f'Returning newly assigned color: {key}:{self.assigned_colors[key]}')
            return color
    
    def assign(self, thing, color):
        """Assigns a specific color to a thing"""
        key = self.make_key(thing)
        self.assigned_colors[key] = color
        if color in self.colors: self.colors.remove(color)

    def many(self, things, color=None):
        for i, t in enumerate(things):
            if color is None and i == 0:
                color = self(t)
            else:
                self.assign(t, color)

