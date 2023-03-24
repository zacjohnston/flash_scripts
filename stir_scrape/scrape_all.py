import pandas as pd
import time 

import scrape_tools
from mass_list import masses

alphas = ['1.25']

max_dat_vars = ['rsh',
                'mdot',
                'turb_antesonic',
                'heat_eff',
                'lnue',
                'lnueb',
                'lnux',
                ]

end_dat_vars = ['rsh',
                'time',
                'pns_m',
                'pns_r',
                'rhoc',
                'etot',
                'ekin',
                'eint',
                'egrav',
                'eexp',
                ]


if __name__ == "__main__":
    t0 = time.time()

    for alpha in alphas:
        table = pd.DataFrame({'mass': masses})

        var_lists = scrape_tools.get_all_dat_scalars(masses=masses,
                                                     alpha=alpha,
                                                     max_dat_vars=max_dat_vars,
                                                     end_dat_vars=end_dat_vars,
                                                     )

        data = pd.DataFrame(var_lists)
        table = pd.concat([table, data], axis=1)

        table['exploded'] = table['end_rsh'] > 5e7  # >500 km

        table.to_csv(f'out/scraped_alpha{alpha}.csv', index=False)

    t1 = time.time()
    print(f'Total scrape time: {t1-t0:.3f} s')

