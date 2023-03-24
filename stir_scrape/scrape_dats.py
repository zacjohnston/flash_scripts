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
    dt = 5e-5  # timestep to interpolate onto
    
    for alpha in alphas:
        dats = scrape_tools.get_dat_tables(dat_vars=dat_vars,
                                           masses=masses,
                                           alpha=alpha,
                                           dt=dt)

        path = f'out/scraped_time_series_alpha{alpha}'
        if not os.path.exists(path):
            os.mkdir(path)

        for mass, table in dats.items():
            filename = f'time_series_alpha{alpha}_{mass}.csv'
            filepath = os.path.join(path, filename)
            table.to_csv(filepath, index=False)

    t1 = time.time()
    print(f'time: {t1 - t0:.3f} s')
