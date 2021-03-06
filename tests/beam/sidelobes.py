"""Plot intensity profile of sidelobes."""
import matplotlib.pyplot as plt
import numpy as np

from frbpoppy.survey import Survey

from tests.convenience import plot_aa_style, rel_path

SIDELOBES = [0, 1, 2, 8]
SURVEY = 'wsrt-apertif'
MIN_Y = 1e-7
n = 50000

plot_aa_style()

for sidelobe in reversed(SIDELOBES):

    args = {'sidelobes': sidelobe}

    s = Survey(SURVEY)
    s.set_beam(model='airy', n_sidelobes=sidelobe)
    int_pro, offset = s.calc_beam(shape=n)

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

    plt.plot(offset, int_pro, label=label)

plt.xlabel(r'Offset ($^{\circ}$)')
plt.ylabel('Intensity Profile')
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig(rel_path('./plots/beam_int_sidelobes.pdf'))
