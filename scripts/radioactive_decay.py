import os
import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
FIGURES = os.path.join(_ROOT, "latex", "figures")

from tools.plots.plot_vector_field import make_phase_diagram
from math import log


def rad_decay_phase(half_life, min_t_per_hl, max_t_per_hl, min_mass, max_mass,
                    pdf_path=None, shade_nonphysical=False,
                    width_frac=1.0, display_frac=1.0, aspect=0.75):
    base_decay_rate = log(2) / half_life
    title = 'Radioactive Decay ODE Solutions'
    xlabel = 'Time (years)'
    ylabel = 'Mass of Isotope'

    min_t = min_t_per_hl * half_life
    max_t = max_t_per_hl * half_life

    y_arr_len_fun = lambda args: -args[0][0] * args[2]

    make_phase_diagram([base_decay_rate], min_t, max_t, min_mass, max_mass,
                       title, xlabel, ylabel, y_arr_len_fun, save_path=pdf_path,
                       shade_nonphysical=shade_nonphysical,
                       width_frac=width_frac, display_frac=display_frac, aspect=aspect)


if __name__ == "__main__":
    rad_decay_phase(1, -0.5, 5, -10, 80,
                    pdf_path=os.path.join(FIGURES, "radioactive_decay.pdf"),
                    shade_nonphysical=True,
                    width_frac=1.0, display_frac=0.48, aspect=0.75)
