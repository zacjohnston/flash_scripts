import pandas as pd
import time
import os

import scrape_tools
from mass_list import masses

if __name__ == "__main__":
    t0 = time.time()
    dat_vars = ['rsh',
                'etot',
                'ekin',
                'eint',
                'egrav',
                'eexp',
                'gain_bind',
                'mdot',
                'rhoc',
                'gain_heat',
                'gain_mass',
                'gain_entr',
                'pns_m',
                'pns_r',
                'lnue',
                'lnueb',
                'lnux',
                'enue',
                'enueb',
                'enux',
                'rmsnue',
                'rmsnueb',
                'rmsnux',
                'rnue',
                'rnueb',
                'rnux',
                'turb_antesonic',
                'heat_eff',
                ]

    mults = [None, '10x', '0.01x']
    mult_masses = ['12.0', '20.0', '40']
    msets = {1: 'LMP', 2: 'LMP+N50', 3: 'IPA'}

    dt = 5e-5  # timestep to interpolate onto

    for mult in mults:
        tabs = {None: [1, 2, 3]}.get(mult, [1, 2])
        mass_list = {None: masses}.get(mult, mult_masses)
        mult_str = {None: ''}.get(mult, f'_{mult}')

        for tab in tabs:
            print(f'Scraping tab{tab}{mult_str}')

            dats = scrape_tools.get_dat(dat_vars=dat_vars,
                                        tab=tab,
                                        masses=mass_list,
                                        mult=mult,
                                        dt=dt)

            mset = msets[tab]
            path = f'./time_series_{mset}{mult_str}'
            if not os.path.exists(path):
                os.mkdir(path)

            for mass, table in dats.items():
                filename = f'time_series_{mset}{mult_str}_{mass}.csv'
                filepath = os.path.join(path, filename)
                table.to_csv(filepath, index=False)

    t1 = time.time()
    print(f'time: {t1 - t0:.3f} s')
