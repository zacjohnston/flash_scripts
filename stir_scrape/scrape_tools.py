import pandas as pd
import numpy as np
import math

from flashbang.simulation import Simulation


# =======================================================
#                    loading models
# =======================================================
def load_model(mass,
               alpha,
               load_all=False,
               load_dat=False,
               load_profiles=False,
               verbose=False):
    """Load model

    Returns : Simulation

    parameters
    ----------
    mass : str
    alpha : str
    load_all : bool
    load_dat : bool
        ignored if load_all=True
    load_profiles : bool
        ignored if load_all=True
    verbose : bool
    """
    run = f'stir2_14may19_s{mass}_alpha{alpha}'
    model = f'run_{mass}'
    model_set = f'run_14may19_a{alpha}'

    sim = Simulation(run=run,
                     model=model,
                     model_set=model_set,
                     load_all=False,
                     config='stir',
                     verbose=verbose,
                     )

    if load_all:
        sim.load_all()
    else:
        if load_dat:
            sim.load_dat()
        if load_profiles:
            sim.load_all_profiles()

    return sim


# =======================================================
#                   dat scalars
# =======================================================
def get_all_dat_scalars(masses,
                        alpha,
                        max_dat_vars,
                        end_dat_vars,
                        ):
    """Return lists of all variables

    Returns : {var: []}

    parameters
    ----------
    masses : [str]
    alpha :str
    max_dat_vars : [str]
    end_dat_vars : [str]
    """
    lists = {}
    var_sets = {'max': max_dat_vars,
                'end': end_dat_vars}

    for prefix, vset in var_sets.items():
        for var in vset:
            lists[f'{prefix}_{var}'] = []

    for mass in masses:
        model = load_model(mass=mass, alpha=alpha, load_dat=True)

        for var in max_dat_vars:
            lists[f'max_{var}'] += [model.dat[var].max()]

        for var in end_dat_vars:
            lists[f'end_{var}'] += [model.dat[var].iloc[-1]]

    return lists


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
        model = load_model(mass=mass, alpha=alpha, load_dat=True)

        for var in dat_vars:
            lists[var] += [model.dat[var].max()]

    return lists


def get_end_dats(dat_vars, masses, alpha):
    """Return list .dat variables at end of simulation

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
        model = load_model(mass=mass, alpha=alpha, load_dat=True)

        for var in dat_vars:
            lists[var] += [model.dat[var].iloc[-1]]

    return lists


# =======================================================
#                      dat
# =======================================================
def get_dat(mass, dat_vars, alpha, dt=5e-5, zero_bounce=True):
    """Returns reduced dat tables from set of models

    Returns: {mass: pd.DataFrame}

    Parameters
    ----------
    mass : str
    dat_vars : [str]
    alpha : str
    dt : float
    zero_bounce : bool
    """
    model = load_model(mass=mass, alpha=alpha, load_dat=True)

    if zero_bounce:
        model.get_bounce_time()
        model.dat['time'] -= model.bounce['time']

    dat = interpolate_dat(dat_table=model.dat,
                          dt=dt,
                          dat_vars=dat_vars)

    return dat


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


# =======================================================
#                      profiles
# =======================================================
def get_nusphere(masses, alpha):
    """Extract nusphere values from profiles

    Returns: {var: []}
    """
    lists = {'zams': masses}

    varlist = ['pns_mass', 'pns_rad', 'pns_dens', 'pns_temp',
               'nu_lum_e', 'nu_lum_eb', 'nu_en_e', 'nu_en_eb',
               'max_s']

    for var in varlist:
        lists[var] = []

    for mass in masses:
        model = load_model(mass=mass, alpha=alpha, load_all=True)

        rnue = model.dat['rnue'].iloc[-1]
        profile = model.profiles.isel(chk=-1)
        dat = model.dat.iloc[-1]

        lists['pns_rad'] += [rnue]
        lists['pns_mass'] += [interp_profile(rnue, 'mass', profile)]
        lists['pns_dens'] += [interp_profile(rnue, 'dens', profile)]
        lists['pns_temp'] += [interp_profile(rnue, 'temp', profile)]

        lists['nu_lum_e'] += [dat['lnue']]
        lists['nu_lum_eb'] += [dat['lnueb']]
        lists['nu_en_e'] += [dat['enue']]
        lists['nu_en_eb'] += [dat['enueb']]

        lists['max_s'] += [float(profile['entr'].max().values)]

    return lists


def interp_profile(radius, var, profile):
    """Interpolate profile variable at specific radius
    """
    return np.interp(radius, profile['r'], profile[var])
