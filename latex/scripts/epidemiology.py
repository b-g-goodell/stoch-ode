import os
import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
FIGURES = os.path.join(_ROOT, "latex", "figures")

from simulation_frameworks.epidemiology import simulate_and_plot

if __name__ == "__main__":
    # state [S, I, R]; params (time_between_interactions, recovery_half_life, infection_prob)
    simulate_and_plot(0, 500, [90, 10, 0], (0.001, 45, 0.0001),
                      pdf_path=os.path.join(FIGURES, "epidemiology.pdf"),
                      width_frac=0.7, display_frac=1.0, aspect=0.7 * 0.75)
