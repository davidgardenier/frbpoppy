"""Plot a log N / log S graph for three different populations."""
import numpy as np
import matplotlib.pyplot as plt

from frbpoppy import CosmicPopulation, Survey, SurveyPopulation

from tests.convenience import plot_aa_style, rel_path

SIZE = 1e5
GAMMAS = [-1.4, 1]


def get_local():
    """Construct a local population."""
    pop = CosmicPopulation.simple(SIZE, generate=True)
    survey = Survey('perfect')
    surv_pop = SurveyPopulation(pop, survey)
    return surv_pop.frbs.s_peak


def get_further(gamma):
    """Construct populations going further out."""
    # Construct populations
    pop = CosmicPopulation.simple(SIZE)
    pop.set_dist(z_max=2.5)
    pop.set_si(model='constant', value=gamma)
    pop.set_lum(model='constant', value=10**42.5)
    pop.generate()

    if gamma == 1:
        pop.set_lum(model='constant', value=10**43)
        pop.gen_lum()

    # Survey populations
    survey = Survey('perfect')
    surv_pop = SurveyPopulation(pop, survey)

    return surv_pop.frbs.s_peak


def get_s_peaks():
    """Get s_peaks of populations."""
    s_peaks = {}

    s_peaks['A'] = get_local()
    s_peaks['B'] = get_further(GAMMAS[0])
    s_peaks['C'] = get_further(GAMMAS[1])

    return s_peaks


def calc_cum_hist(s_peaks):
    """Get the x,y for a cumulative histogram of given s_peaks."""
    data = {}
    for s in s_peaks:
        # Bin up
        s_peak = s_peaks[s]
        min_f = np.log10(min(s_peak))
        max_f = np.log10(max(s_peak))
        log_bins = np.logspace(min_f, max_f, 50)
        hist, edges = np.histogram(s_peak, bins=log_bins)
        n_gt_s = np.cumsum(hist[::-1])[::-1]

        x = edges[:-1]
        y = n_gt_s

        data[s] = (x, y)

    return data


def plot_logn_logs(data):
    """Plot log N log S data in a cumlative histogram."""
    plot_aa_style()

    fig, (ax1) = plt.subplots(1, 1)

    for key in data:
        x, y = data[key]
        ax1.step(x, y, where='post', label=key)

    plt.xlabel(r'S$_{\text{min}}$ (Jy)')
    plt.ylabel(r'N(${>}\text{S}_{\text{min}}$)')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim((1e-3, 1e1))
    plt.legend()
    plt.tight_layout()
    plt.savefig(rel_path('plots/logn_logs_abc.pdf'))


def main():
    """Run."""
    s_peaks = get_s_peaks()
    data = calc_cum_hist(s_peaks)
    plot_logn_logs(data)


if __name__ == '__main__':
    main()
