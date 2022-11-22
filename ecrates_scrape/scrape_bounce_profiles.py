import pandas as pd
import time
import os

import scrape_tools
from mass_list import masses

if __name__ == "__main__":
    t0 = time.time()
    profile_vars = ['r',
                    'mass',
                    'dens',
                    'pres',
                    'temp',
                    'entr',
                    'ye',
                    'yl',
                    'gpot',
                    'velx',
                    ]

    mults = [None, '10x', '0.01x']
    mult_masses = ['12.0', '20.0', '40']
    msets = {1: 'LMP', 2: 'LMP+N50', 3: 'IPA'}

    for mult in mults:
        tabs = {None: [1, 2, 3]}.get(mult, [1, 2])
        mass_list = {None: masses}.get(mult, mult_masses)
        mult_str = {None: ''}.get(mult, f'_{mult}')

        for tab in tabs:
            print(f'Scraping tab{tab}{mult_str}')

            profiles = scrape_tools.get_bounce_profiles(profile_vars=profile_vars,
                                                        tab=tab,
                                                        masses=mass_list,
                                                        mult=mult)

            mset = msets[tab]
            path = f'./bounce_profiles_{mset}{mult_str}'
            if not os.path.exists(path):
                os.mkdir(path)

            for mass, table in profiles.items():
                filename = f'bounce_profile_{mset}{mult_str}_{mass}.csv'
                filepath = os.path.join(path, filename)
                table.to_csv(filepath, index=False)

    t1 = time.time()
    print(f'time: {t1 - t0:.3f} s')
