import os
import time 
import matplotlib.pyplot as plt

import scrape_tools
from mass_list import masses


if __name__ == "__main__":
    t0 = time.time()

    path = f'out/profile_plots'
    alpha = '1.25'
    profile_vars = ['mach']
    x_var = 'r'
    x_lims = [1e1, 2e4]
    y_lims = [-0.1, 1.2]

    if not os.path.exists(path):
        os.mkdir(path)

    fig, ax = plt.subplots()

    for mass in masses:
        for var in profile_vars:
            print(f'Plotting profile for mass={mass}')
            model = scrape_tools.load_model(mass=mass, alpha=alpha, load_all=True)

            model.plot_profile(chk='last',
                               y_var=var,
                               x_var=x_var,
                               x_lims=x_lims,
                               y_lims=y_lims,
                               ax=ax)

            filename = f'profile_{var}_{mass}.png'
            filepath = os.path.join(path, filename)

            fig.savefig(filepath)
            ax.clear()

    plt.close(fig)
    t1 = time.time()
    print(f'time: {t1-t0:.3f} s')

