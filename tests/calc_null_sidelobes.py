"""Calculate where null points of an Airy pattern lie."""
from scipy.special import j1
import matplotlib.pyplot as plt
import numpy as np
import os


STEPSIZE = 1e-6
PLOT = True

x_range = np.arange(0, 50, STEPSIZE)
y_range = 4*(j1(x_range)/x_range)**2
nulls = []

# Find where curve changes direction
ind = np.diff(np.sign(np.diff(y_range)))
x_null = x_range[1:-1][ind > 0]
y_null = y_range[1:-1][ind > 0]

print(x_null)

if PLOT:
    title = r"Bessel function over $\text{x}$"

    # Change working directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Use A&A styling for plots
    plt.style.use('./aa.mplstyle')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(title)
    plt.plot(x_range[::10], y_range[::10])
    plt.scatter(x_null, y_null)
    plt.yscale('log')
    plt.tight_layout()

    plt.savefig('./plots/null_sidelobes.pdf')
