"""Check ratios of rates."""
from frbpoppy import CosmicPopulation, Survey, SurveyPopulation
from frbpoppy import unpickle, pprint, plot

MAKE = False

if MAKE:
    # Create cosmic population
    n_per_day = 5000
    days = 30
    cosmic = CosmicPopulation(n_per_day*days,
                              lum_range=[1e39, 1e49],
                              lum_index=-0.5,
                              pulse_model='lognormal',
                              pulse_mu=1.,
                              pulse_sigma=1.,
                              name='neg_cosmic')
    pprint(cosmic.name)
    cosmic.save()
else:
    cosmic = unpickle('neg_cosmic')

pops = []

for name in ['htru']:

    # Set up beam patterns
    if name == 'htru':
        survey = Survey(name.upper(), gain_pattern='parkes')
    elif name == 'apertif':
        survey = Survey(name.upper(), gain_pattern='apertif')
    else:
        survey = Survey(name.upper(), gain_pattern='airy', sidelobes=0.5)

    surv_pop = SurveyPopulation(cosmic, survey)
    pops.append(surv_pop)

plot(*pops, frbcat='htru')
