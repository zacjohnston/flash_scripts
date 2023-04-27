import pandas as pd
import time 

import scrape_tools
from mass_list import masses


if __name__ == "__main__":
    t0 = time.time()
    alphas = ['1.25']

    for alpha in alphas:
        var_lists = scrape_tools.get_nuwind(masses=masses, alpha=alpha)

        table = pd.DataFrame(var_lists)
        table.to_csv(f'out/nusphere_alpha{alpha}.csv', index=False)

    t1 = time.time()
    print(f'time: {t1-t0:.3f} s')

