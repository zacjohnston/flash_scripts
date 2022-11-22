import pandas as pd
import time 

import scrape_tools
from mass_list import masses


if __name__ == "__main__":
    t0 = time.time()
    dat_vars = ['rsh',
                'mdot',
                'turb_antesonic',
                ]
    alphas = ['1.25']

    for alpha in alphas:
        table = pd.DataFrame({'mass': masses})

        var_lists = scrape_tools.get_max_dats(dat_vars=dat_vars,
                                              masses=masses,
                                              alpha=alpha)

        data = pd.DataFrame(var_lists)
        table = pd.concat([table, data], axis=1)

        table.to_csv(f'out/max_dats_alpha{alpha}.csv', index=False)

    t1 = time.time()
    print(f'time: {t1-t0:.3f} s')

