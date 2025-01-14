# -*- mode: python -*-

#This code is based on: https://github.com/mishagrol/TernaryPlotPy

"""A triangle-plot general class, meant to support the soil texture triangle. 
   Written by C. P. H. Lewis while at the University of California, Berkeley, 2008-2009. """

import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import pandas as pd

class SoilTrianglePlot:
    """For plotting soil texture data (e.g., sand, silt, clay) on a ternary plot."""


    def _toCart(self, threecoords):
        """
        Converts the soil texture triangle coordinates (sand, silt, clay) 
        to Cartesian coordinates for plotting.
        """
        cartxs = []
        cartys = []
        for triple in threecoords:
            b, l, r = triple  # b = sand, l = clay, r = silt (correct order)
        #assert (b + l + r == 100), "3-coordinate values must sum to 100; %d, %d, %d don't" % (b, l, r)
            total = b + l + r
            b2 = b * (100 / total)
            l2 = l * (100 / total)
            r2 = r * (100 / total)
            cartxs.append(100 - b2 - l2 / 2.0)
            cartys.append(sqrt(3) * l2 / 2.0)
        return (cartxs, cartys)

    def scatter(self, threecoords, **kwargs):
        """Scatter plot the soil texture data."""
        xs, ys = self._toCart(threecoords)
        plt.scatter(xs, ys, **kwargs)

    def plot(self, threecoords, descriptor, **kwargs):
        """Plot the soil texture data."""
        xs, ys = self._toCart(threecoords)
        plt.plot(xs, ys, descriptor, **kwargs)

    def colorbar(self, label):
        """Draw a colorbar and label it."""
        cb = plt.colorbar()
        cb.set_label(label)

    def line(self, begin, end, simplestyle='k-', **kwargs):
        """Draw a line between two points on the triangle."""
        xs, ys = self._toCart([begin, end])
        plt.plot(xs, ys, simplestyle, **kwargs)

    def outline(self):
        """Draw the outline of the soil texture triangle."""
        self.line((0, 100, 0), (100, 0, 0), 'k-')
        self.line((0, 100, 0), (0, 0, 100), 'k-')
        self.line((0, 0, 100), (100, 0, 0), 'k-')

    def grid(self, triple=([25, 50, 100], [25, 50, 100], [25, 50, 100]), labels=()):
        """Draw grid lines for the soil texture triangle."""
        (bs, ls, rs) = triple
        lstyle = {'dashes': (1, 1), 'linewidth': 0.5}
        for b in bs:
            self.line((b, 0, 100 - b), (b, 100 - b, 0), **lstyle)
            plt.text(100 - b, -5, b, rotation=300, fontsize=9)
        for l in ls:
            self.line((0, l, 100 - l), (100 - l, l, 0), **lstyle)
            plt.text(l / 2.0 - 2 * len(str(l)), sqrt(3) * l / 2 - 1, l, fontsize=9)
        for r in rs:
            self.line((0, 100 - r, r), (100 - r, 0, r), **lstyle)
            plt.text(50 + r / 2.0, sqrt(3) * (50 - r / 2.0), r, rotation=60, fontsize=9)
        if len(labels) > 0:
            plt.text(50 - len(labels[0]) / 2, -12, labels[0], fontsize=8)
            plt.text(15 - len(labels[1]) / 2, sqrt(3) * (25 - len(labels[1]) / 2), labels[1], rotation=60, fontsize=8)
            plt.text(82 - len(labels[2]) / 2, 48 - len(labels[2]) / 2, labels[2], rotation=300, fontsize=8)

    def soil_categories(self, sclabel = '_nolegend_', country = 'Britain'):
        """ Draws dashed lines between the soil-type categories. These are regional; options  are:
        'USA' (boundaries estimated from Brady & Weil, 12th ed, fig 4.7.)
        'Britain' (boundaries estimated from White, _Principles and Practices of Soil Science, 2006, fig. 2.3.a
        'Australia' (boundaries estimated from White, ibid., fig. 2.3.b)."""
        self.grid((range(10, 100, 10), range(10, 100, 10), range(10, 100, 10)))
        lstyle = {'dashes': (4, 1, 2, 1),
         'linewidth': 1.5}
        if country=='USA':
            self.line((85, 0, 15), (90, 10, 0), **lstyle)
            self.line((70, 0, 30), (85, 15, 0), **lstyle)
            self.line((50, 0, 50), (23, 27, 50), **lstyle)
            self.line((20, 0, 80), (10, 10, 80), **lstyle)
            self.line((10, 10, 80), (0, 10, 90), **lstyle)
            self.line((80, 20, 0), (52, 20, 28), **lstyle)
            self.line((52, 20, 28), (45, 27, 28), **lstyle)
            self.line((45, 27, 28), (0, 27, 73), **lstyle)
            self.line((52, 20, 28), (52, 6, 42), **lstyle)
            self.line((52, 6, 42), (44, 6, 50), **lstyle)
            self.line((45, 27, 28), (45, 55, 0), **lstyle)
            self.line((65, 35, 0), (45, 35, 20), **lstyle)
            self.line((45, 40, 15), (0, 40, 60), **lstyle)
            self.line((20, 27, 53), (20, 40, 40), **lstyle)
            self.line((20, 40, 40), (0, 60, 40), label=sclabel, **lstyle)
        if country== 'Britain':
            self.line((85, 0, 15), (90, 10, 0), **lstyle)
            self.line((70, 0, 30), (85, 15, 0), **lstyle)
            self.line((82,18,0),(0,18,82), **lstyle)
            self.line((70,30,0),(50,30,20),**lstyle)
            self.line((50,30,20),(50,0,50), **lstyle)
            self.line((20,35,45),(20,0,80), **lstyle)
            self.line((0,55,45),(20,35,45), **lstyle)
            self.line((45,35,20),(0,35,65), **lstyle)
            self.line((45,35,20),(50,30,20),**lstyle)
            self.line((45,35,20),(45,55,0), **lstyle)
        if country == 'Australia':
            self.line((0,75,25),(75,0,25), **lstyle)
            self.line((35,40,25),(0,40,60), **lstyle)
            self.line((50,25,25),(0,25,75), **lstyle)
            self.line((50,25,25),(82,18,0), **lstyle)
            self.line((35,40,25),(72,28,0), **lstyle)
            self.line((92,0,8),(87,9,4), **lstyle)
            self.line((91.5,8.5,0),(63,12,25),**lstyle)
            self.line((76.25, 10.5, 13.25),(50,50,0),**lstyle)
        labels = ('Sand (%)', 'Clay (%)', 'Silt (%)')
        plt.text(40 - len(labels[0]) / 2, -10, labels[0])
        plt.text(13 - len(labels[1]) / 2, sqrt(3) * (25 - len(labels[1]) / 2), labels[1], rotation=60)
        plt.text(80 - len(labels[2]) / 2, 50 - len(labels[2]) / 2, labels[2], rotation=300)
    
    def patch(self, limits, **kwargs):
        """Fill the area bounded by limits."""
        coords = []
        for pt in [[1, -1, 1], [1, 0, -1], [-1, 0, 0], [1, -1, 0]]:
            for i in [0, 1, 2]:
                if pt[i] == 1:
                    pt[i] = limits[i][1]
                elif pt[i] == 0:
                    pt[i] = limits[i][0]
            coords.append(pt)
        coords.append(coords[0])  # Close the loop
        xs, ys = self._toCart(coords)
        plt.fill(xs, ys, **kwargs)

    def scatter_from_csv(self, filename, sand='sand', silt='silt', clay='clay', diameter='', hue='', tags='', **kwargs):
        """Load data from a CSV file and plot it."""
        soilrec = pd.read_csv(filename)
        if sand not in soilrec or silt not in soilrec or clay not in soilrec:
            print("ERROR: Columns for sand, silt, and clay not found in CSV.")
            return
        locargs = {'s': None, 'c': None}
        for col, key in ((diameter, 's'), (hue, 'c')):
            if col and col in soilrec:
                locargs[key] = soilrec[col]
        values = list(zip(soilrec[sand], soilrec[clay], soilrec[silt] ))
        xs, ys = self._toCart(values)
        plt.scatter(xs, ys, label='_', **locargs)
        if tags:
            for x, y, tag in zip(xs, ys, soilrec[tags]):
                plt.text(x + 1, y + 1, tag, fontsize=8)

    def __init__(self, stitle=''):
        """Initialize the plot with an optional title."""
        plt.clf()
        plt.axis('off')
        plt.axis('equal')
        plt.title(stitle)
        self.outline()

    def text(self, loctriple, word, **kwargs):
        """Add text at a specific location on the plot."""
        x, y = self._toCart([loctriple])
        plt.text(x[0], y[0], word, **kwargs)

    def show(self, filename='trianglegraph_test'):
        """Save and show the plot."""
        plt.axis([-10, 110, -10, 110])
        plt.ylim(-10, 100)
        plt.savefig(filename)
        plt.show()

    def close(self):
        """Close the plot."""
        plt.close()

# Example usage to create and show a ternary plot
if __name__ == "__main__":
    plotter = SoilTrianglePlot("Soil Texture Plot")
    plotter.scatter([(40, 40, 20), (20, 60, 20), (30, 30, 40)]) #N.B. THIS TAKES VALUES IN THE ORDER SAND, CLAY, SILT
    plotter.soil_categories('Britain')
    plotter.show("soil_texture_plot_with_grid_and_categories.png")