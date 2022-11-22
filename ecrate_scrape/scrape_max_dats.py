import pandas as pd
import time 

import scrape_tools
from mass_list import masses


if __name__ == "__main__":
    t0 = time.time()
    dat_vars = ['rsh',
                'lnue',
                'lnua',
                'lnux',
                'mdot',
                ]

    mults = [None, '10x', '0.01x']
    mult_masses = ['12.0', '20.0', '40']

    for mult in mults:
        tabs = {None: [1, 2, 3]}.get(mult, [1, 2])
        mass_list = {None: masses}.get(mult, mult_masses)
        mult_str = {None: ''}.get(mult, f'_{mult}')

        for tab in tabs:
            print(f'Scraping tab{tab}{mult_str}')
            table = pd.DataFrame({'mass': mass_list})

            var_lists = scrape_tools.get_max_dats(dat_vars=dat_vars,
                                                  tab=tab,
                                                  masses=mass_list,
                                                  mult=mult)
            data = pd.DataFrame(var_lists)
            table = pd.concat([table, data], axis=1)

            table.to_csv(f'max_dats_tab{tab}{mult_str}.csv', index=False)

    t1 = time.time()
    print(f'time: {t1-t0:.3f} s')

