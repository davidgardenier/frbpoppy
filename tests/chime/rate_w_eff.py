"""Plot effective pulse width against rate for CHIME repeaters.

For Fig. 3 of 'Beaming as an explanation of the repetition/width relation
in FRBs'
"""
from scipy.integrate import quad
from scipy.stats import chi2, norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from frbcat import Frbcat
from tests.convenience import plot_aa_style, rel_path

SCALE = 'log'


def import_frbcat():
    """Gather rate data."""
    cat = Frbcat()
    cat.clean()
    cat.filter(one_offs=False,
               repeaters=True,
               repeat_bursts=True,
               one_entry_per_frb=True)
    df = cat.df

    # Remove Pushichino events
    df = df[~df.telescope.str.startswith('pushchino')]

    # Keep CHIME
    df = df[df.telescope.str.startswith('chime')]

    # Collate exposure time information
    #              Name, Number of Bursts, Exposure [h]
    rep_data = {'FRB180725.J0613+67': [np.nan, np.nan],
                'FRB180814.J0422+73': [3, 14],
                'FRB180908.J1232+74': [4, (.5*(53+36))],
                'FRB180916.J0158+65': [10, 23],
                'FRB181017.J1705+68': [2, 20],
                'FRB181017.J18+81': [3, (.5*(55+159))],
                'FRB181030.J1054+73': [2, (.5*(27+19))],
                'FRB181119.J12+65': [3, 19],
                'FRB181128.J0456+63': [2, 16],
                'FRB190110.J1353+48': [3, 23],
                'FRB190116.J1249+27': [2, 8],
                'FRB190117.J2207+17': [5, 19],
                'FRB190208.J1855+46': [2, 20],
                'FRB190209.J0937+77': [2, (.5*(34+28))],
                'FRB190212.J02+20': [2, 17],
                'FRB190222.J2052+69': [2, 20],
                'FRB190417.J1939+59': [3, 29],
                'FRB190604.J1435+53': [2, 30],
                'FRB190907.J08+46': [3, 23]}
    db = pd.DataFrame(rep_data, index=['n_bursts', 'exposure']).T
    db['rate'] = db.n_bursts / db.exposure
    db['frb_name'] = db.index

    # Add info to frbcat
    df['rate'] = np.nan
    for name, row in db.iterrows():
        df.loc[df.frb_name == name, 'rate'] = row.rate
        df.loc[df.frb_name == name, 'n_bursts'] = row.n_bursts
        df.loc[df.frb_name == name, 'exposure'] = row.exposure

    return df


def poisson_interval(k, sigma=1):
    """
    Use chi-squared info to get the poisson interval.

    Given a number of observed events, which range of observed events would
    have been just as likely given a particular interval?

    Based off https://stackoverflow.com/questions/14813530/
    poisson-confidence-interval-with-numpy
    """
    gauss = norm(0, 1).pdf
    a = 1 - quad(gauss, -sigma, sigma, limit=1000)[0]
    low, high = (chi2.ppf(a/2, 2*k) / 2, chi2.ppf(1-a/2, 2*k + 2) / 2)
    if isinstance(k, np.ndarray):
        low[k == 0] = 0.
    elif k == 0:
        low = 0.0

    return low, high


def plot_w_eff_rate(df):
    """Plot effective pulse width against rate."""
    plot_aa_style(cols=1)

    df = df.sort_values('utc')

    # Groupby repeater
    db = df
    # db = df.groupby(['frb_name']).mean()
    width = db.width
    width_err = (db.width_error_lower, db.width_error_upper)
    n_bursts = db.n_bursts
    rate = db.rate
    exposure = db.exposure.to_numpy()

    # Calculate error bars
    low, high = poisson_interval(n_bursts.to_numpy(), sigma=1)
    rate_err = (low/exposure, high/exposure)

    # Plot values
    plt.errorbar(width, rate, xerr=width_err, yerr=rate_err,
                 marker='x', fmt='o')

    # Print correlation
    _width = width[~np.isnan(rate)]
    _rate = rate[~np.isnan(rate)]
    r = np.corrcoef(_width, _rate)[0, 1]
    print('Pearson correlation coefficient: ', r)
    r = np.corrcoef(np.log10(_width), np.log10(_rate))[0, 1]
    print('Pearson correlation coefficient in log10 space: ', r)

    plt.xlabel(r'Pulse Width (ms)')
    plt.ylabel(r'Rate (/hour)')

    if SCALE == 'log':
        plt.xscale('log')
        plt.yscale('log', nonposy='clip')

    plt.tight_layout()
    plt.savefig(rel_path('./plots/rate_w_eff_chime.pdf'))

    # Save data
    a = np.asarray([width, width_err[0], width_err[1],
                    rate, rate_err[0], rate_err[1]]).T
    np.savetxt(rel_path('./plots/chime_rep_width.csv'), a, delimiter=",",
               header=','.join(['w_eff', 'w_eff_lower_err', 'w_eff_upper_err',
                                'rate', 'rate_lower_err', 'rate_upper_err']))


if __name__ == '__main__':
    df = import_frbcat()
    plot_w_eff_rate(df)
