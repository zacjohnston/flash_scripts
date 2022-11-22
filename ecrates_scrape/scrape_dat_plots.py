import os
import time 
import matplotlib.pyplot as plt

import scrape_tools
from plotRoutines import tools
from mass_list import masses


if __name__ == "__main__":
    t0 = time.time()
    dat_vars = ['rsh',
                'heat_eff',
                ]

    y_scales = {'rsh': 'log'}
    tabs = [1, 2, 3]

    path = tools.ecrate_path()
    scrape_path = os.path.join(path, 'plotRoutines', 'scrape')

    for var in dat_vars:
        dirpath = os.path.join(scrape_path, f'plot_dats')
        tools.try_mkdir(dirpath)

    for mass in masses:
        print(f'Scraping mass {mass}')
        comp = tools.load_comparison(mass=mass, tabs=tabs)
        fig = comp.plot_dats(dat_vars)

        for i, var in enumerate(dat_vars):
            y_scale = y_scales.get(var)
            if y_scale is not None:
                fig.axes[i].set_yscale(y_scale)

        filename = f'dats_{mass}.png'
        filepath = os.path.join(scrape_path, f'plot_dats', filename)

        fig.savefig(filepath)
        plt.close(fig)

    t1 = time.time()
    print(f'time: {t1-t0:.3f} s')

