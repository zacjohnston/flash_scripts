import time
import os

import scrape_tools
from mass_list import masses

if __name__ == "__main__":
    t0 = time.time()

    dat_vars = ['rsh', 'etot', 'ekin', 'eint', 'egrav', 'eexp',
                'gain_bind', 'mdot', 'rhoc', 'gain_heat', 'gain_mass',
                'gain_entr', 'pns_m', 'pns_r', 'lnue', 'lnueb', 'lnux',
                'enue', 'enueb', 'enux', 'rmsnue', 'rmsnueb', 'rmsnux',
                'rnue', 'rnueb', 'rnux', 'turb_antesonic', 'heat_eff']

    alphas = ['1.25']
    # masses = ['20.0', '40']
    dt = 1e-3  # timestep to interpolate onto

    for alpha in alphas:
        path = f'out/scraped_time_series_alpha{alpha}'

        if not os.path.exists(path):
            os.mkdir(path)

        for mass in masses:
            print(f'Extracting dat for alpha={alpha}, mass={mass}')
            dat = scrape_tools.get_dat(mass=mass,
                                       dat_vars=dat_vars,
                                       alpha=alpha,
                                       dt=dt)

            filename = f'time_series_alpha{alpha}_{mass}.csv'
            filepath = os.path.join(path, filename)
            dat.to_csv(filepath, index=False)

    t1 = time.time()
    print(f'time: {t1 - t0:.3f} s')
