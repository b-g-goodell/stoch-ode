import os
import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
FIGURES = os.path.join(_ROOT, "latex", "figures")

from simulation_frameworks.allee_effect import plot_extinction_and_survival, generate_allee_heatmap
from tools.plots.plot_vector_field import make_phase_diagram
from math import log

if __name__ == "__main__":
    sample_size = 128
    init_t = 0
    sim_t = 2000
    init_st = 50
    base_birth_rate = 0.0045
    base_doubling_time = log(2)/base_birth_rate
    coop = 50
    cap = 200
    params = (base_doubling_time, coop, cap)

    style = dict(width_frac=0.7, display_frac=1.0, aspect=0.7 * 0.75)
    plot_extinction_and_survival(init_t, sim_t, init_st, params,
                                  pdf_path=os.path.join(FIGURES, "allee_effect_two_trajs.pdf"),
                                  **style)

    generate_allee_heatmap(init_t, sim_t, init_st, params, sample_size,
                           pdf_path=os.path.join(FIGURES, "allee_effect.pdf"), **style)

    # Phase diagram: dX/dt = -r*X*(1 - X/L)*(1 - X/K)
    # params_list = [r, L, K]
    allee_ode_params = [base_birth_rate, float(coop), float(cap)]
    allee_ode = lambda args: -args[0][0] * args[2] * (1.0 - args[2]/args[0][1]) * (1.0 - args[2]/args[0][2])

    make_phase_diagram(allee_ode_params, 0, sim_t, -25, 250,
                       'Allee Effect ODE Solutions', 'Time (days)', 'Population',
                       allee_ode,
                       save_path=os.path.join(FIGURES, "allee_ode.pdf"),
                       shade_nonphysical=True, **style)
