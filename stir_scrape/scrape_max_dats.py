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
                'turb_antesonic',
                ]

    table = pd.DataFrame({'mass': masses})

    var_lists = scrape_tools.get_max_dats(dat_vars=dat_vars, masses=masses)

    data = pd.DataFrame(var_lists)
    table = pd.concat([table, data], axis=1)

    table.to_csv(f'out/max_dats.csv', index=False)

    t1 = time.time()
    print(f'time: {t1-t0:.3f} s')

