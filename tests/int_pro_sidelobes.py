"""Plot intensity profile of sidelobes."""
import matplotlib.pyplot as plt
import numpy as np
import os

from frbpoppy.survey import Survey

SIDELOBES = [0, 1, 2, 8]
SURVEY = 'apertif'
MIN_Y = 1e-7
n = 50000

# Change working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

plt.style.use('./aa.mplstyle')

for sidelobe in reversed(SIDELOBES):

    args = {'sidelobes': sidelobe}

    s = Survey(SURVEY, gain_pattern='airy', n_sidelobes=sidelobe)

    int_pro, offset = s.intensity_profile(shape=n)

    # Sort the values
    sorted_int = np.argsort(offset)
    int_pro = int_pro[sorted_int]
    offset = offset[sorted_int]

    # Clean up lower limit
    offset = offset[int_pro > MIN_Y]
    int_pro = int_pro[int_pro > MIN_Y]

    label = f'{sidelobe} sidelobes'
    if sidelobe == 1:
        label = label[:-1]

    # Offset in degrees
    offset = offset/60.

    plt.plot(offset, int_pro, label=label)

plt.xlabel(r'Offset ($\degree$)')
plt.ylabel('Intensity Profile')
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('plots/int_pro_sidelobes.pdf')
