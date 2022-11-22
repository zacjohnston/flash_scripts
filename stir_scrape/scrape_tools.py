import pandas as pd
import numpy as np
import math

from flashbang.simulation import Simulation


# =======================================================
#                    loading models
# =======================================================
def load_model(mass,
               alpha,
               load_all=True):
    """Load model

    Returns : Simulation

    parameters
    ----------
    mass : str
    alpha : str
    load_all : bool
    """
    run = f'stir2_14may19_s{mass}_alpha{alpha}'
    model = f'run_{mass}'
    model_set = f'run_14may19_a{alpha}'

    sim = Simulation(run=run,
                     model=model,
                     model_set=model_set,
                     load_all=load_all,
                     config='stir')

    return sim


# =======================================================
#                   max values
# =======================================================
def get_max_dats(dat_vars, masses, alpha):
    """Return list of max values of .dat variables

    Returns : {var: []}

    parameters
    ----------
    dat_vars : [str]
    masses : [str]
    alpha :str
    """
    lists = {}
    for var in dat_vars:
        lists[var] = []

    for mass in masses:
        model = load_model(mass=mass, alpha=alpha, load_all=False)
        model.load_dat()

        for var in dat_vars:
            lists[var] += [model.dat[var].max()]

    return lists


def get_max_times(dat_vars, masses, alpha):
    """Return list of times of max values of .dat variables

    Returns : {var: []}

    parameters
    ----------
    dat_vars : [str]
    masses : [str]
    alpha :str
    """
    lists = {}
    for var in dat_vars:
        lists[var] = []

    for mass in masses:
        model = load_model(mass=mass, alpha=alpha, load_all=False)
        model.load_dat()

        for var in dat_vars:
            idx = model.dat[var].idxmax()
            lists[var] += [model.dat.loc[idx, 'time']]

    return lists


# =======================================================
#                      dat
# =======================================================
def get_dat(dat_vars, masses, alpha, dt=5e-5):
    """Returns reduced dat tables from set of models

    Returns: {mass: pd.DataFrame}

    Parameters
    ----------
    dat_vars : [str]
    masses : [str]
    alpha : str
    dt : float
    """
    dats = {}

    for mass in masses:
        model = load_model(mass=mass, alpha=alpha)
        model.load_dat()

        dats[mass] = interpolate_dat(dat_table=model.dat,
                                     dt=dt,
                                     dat_vars=dat_vars)

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
