import os
import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
FIGURES = os.path.join(_ROOT, "latex", "figures")

from simulation_frameworks.saline_tank import dg_simulate_tank_ode, INIT_TIME, SIM_TIME, INIT_STATE, PARAMS
from tools.plots.plot_trajectories import plot_trajs

if __name__ == "__main__":
    trajs = [dg_simulate_tank_ode()]
    title = 'Saline Tank Simulation Trajectory'
    xlabel = 'Time (s)'
    ylabel = 'Number of Salt Molecules in Tank'
    plot_kwargs = dict(min_t=INIT_TIME, max_t=SIM_TIME, min_st=0, max_st=500,
                       trajs=trajs, title=title, xlabel=xlabel, ylabel=ylabel)

    plot_trajs(**plot_kwargs, save_path=os.path.join(FIGURES, "saline_tank.pdf"),
               width_frac=0.7, display_frac=1.0, aspect=0.7 * 0.75)
