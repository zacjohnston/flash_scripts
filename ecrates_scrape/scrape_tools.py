import pandas as pd
import numpy as np
import math

from flashbang.simulation import Simulation


# =======================================================
#                    loading models
# =======================================================
def load_model(tab, mass, mult=None):
    """Load model

    Returns : Simulation
    """
    run = f'stir_ecrates_tab{tab}_s{mass}_alpha1.25'
    model = f'run_{mass}'

    mult_str = {None: '_'}.get(mult, f'_{mult}_')
    model_set = f'run_ecrates{mult_str}tab{tab}'

    model = Simulation(run=run,
                       model=model,
                       model_set=model_set,
                       config='stir'
                       )
    return model


# =======================================================
#                      bounce vars
# =======================================================
def get_bounce_vars(bounce_vars, tab, masses, mult=None):
    """Returns lists of bounce variables from set of models

    Returns: {var: []}

    Parameters
    ----------
    bounce_vars : [str]
    tab : int
    masses : [str]
    mult : str
    """
    lists = {}
    for var in bounce_vars:
        lists[var] = []

    for mass in masses:
        model = load_model(tab=tab, mass=mass, mult=mult)

        for var in bounce_vars:
            lists[var] += [model.bounce[var]]

    return lists


def get_bounce_shock(shock_vars, tab, masses, mult=None):
    """Returns lists of shock variables at bounce from set of models

    Returns: {var: []}

    Parameters
    ----------
    shock_vars : [str]
    tab : int
    masses : [str]
    mult : str
    """
    lists = {}
    for var in shock_vars:
        lists[var] = []

    for mass in masses:
        model = load_model(tab=tab, mass=mass, mult=mult)

        for var in shock_vars:
            core_mass = model.bounce['core_mass']
            bounce_profile = model.profiles.sel(chk=model.bounce['chk'])

            shock_val = np.interp(core_mass,
                                  bounce_profile['mass'],
                                  bounce_profile[var])

            lists[var] += [shock_val]

    return lists


# =======================================================
#                   max mdot
# =======================================================
def get_max_dats(dat_vars, tab, masses, mult=None):
    """Return list of max values of .dat variables

    Returns : {var: []}
    """
    lists = {}
    for var in dat_vars:
        lists[var] = []

    for mass in masses:
        model = load_model(tab=tab, mass=mass, mult=mult)

        for var in dat_vars:
            lists[var] += [model.dat[var].max()]

    return lists


# =======================================================
#                   max times
# =======================================================
def get_max_times(dat_vars, tab, masses, mult=None):
    """Return list of times of max values of .dat variables

    Returns : {var: []}
    """
    lists = {}
    for var in dat_vars:
        lists[var] = []

    for mass in masses:
        model = load_model(tab=tab, mass=mass, mult=mult)

        for var in dat_vars:
            idx = model.dat[var].idxmax()
            lists[var] += [model.dat.loc[idx, 'time']]

    return lists


# =======================================================
#                      bounce profile
# =======================================================
def get_bounce_profiles(profile_vars, tab, masses, mult=None):
    """Returns bounce profiles from set of models

    Returns: {mass: pd.DataFrame}

    Parameters
    ----------
    profile_vars : [str]
    tab : int
    masses : [str]
    mult : str
    """
    profiles = {}

    for mass in masses:
        model = load_model(tab=tab, mass=mass, mult=mult)

        bounce_profile = model.profiles.sel(chk=model.bounce['chk'])
        table = bounce_profile.to_dataframe()
        table = table[profile_vars].dropna()

        profiles[mass] = table

    return profiles


# =======================================================
#                      bounce profile
# =======================================================
def get_dat(dat_vars, tab, masses, mult=None, dt=5e-5):
    """Returns reduced dat tables from set of models

    Returns: {mass: pd.DataFrame}

    Parameters
    ----------
    dat_vars : [str]
    tab : int
    masses : [str]
    mult : str
    dt : float
    """
    dats = {}

    for mass in masses:
        model = load_model(tab=tab, mass=mass, mult=mult)
        dats[mass] = interpolate_dat(dat_table=model.dat, dt=dt, dat_vars=dat_vars)

    return dats


def interpolate_dat(dat_table, dt, dat_vars):
    """Interpolates dat table onto regular timesteps

    Returns: pd.DataFrame

    parameters
    ----------
    dat_table : pd.DataFrame
    dt : float
        timestep size to interpolate onto (s)
    dat_vars : [str]
    """
    t_end = dat_table.time.iloc[-1]
    t_end = math.floor(t_end/dt) * dt  # last timestep before t_end
    n_steps = int(t_end/dt + 1)

    timesteps = np.linspace(0, t_end, n_steps)
    table = pd.DataFrame()
    table['time'] = timesteps

    for var in dat_vars:
        table[var] = np.interp(timesteps, dat_table['time'], dat_table[var])

    return table
