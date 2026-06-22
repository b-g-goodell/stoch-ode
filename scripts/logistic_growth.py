import os
import sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
FIGURES = os.path.join(_ROOT, "latex", "figures")

from simulation_frameworks.logistic_growth import (
    log_growth_phase,
    log_growth_mean_vs_ode,
    LOGISTIC_SIMULATION_START_TIME, LOGISTIC_SIMULATION_RUN_TIME,
    BASE_DOUBLING_TIME, CAPACITY, MEAN_VS_ODE_SAMPLE_SIZE,
)

if __name__ == "__main__":
    log_growth_phase(
        BASE_DOUBLING_TIME, CAPACITY,
        LOGISTIC_SIMULATION_START_TIME / BASE_DOUBLING_TIME,
        LOGISTIC_SIMULATION_RUN_TIME / BASE_DOUBLING_TIME,
        -25,
        225,
        pdf_path=os.path.join(FIGURES, "logistic_growth.pdf"),
        shade_nonphysical=True,
        width_frac=1.0, display_frac=0.48, aspect=0.75,
        xlabel='Time (days)',
        ylabel='Population',
    )

    log_growth_mean_vs_ode(
        sample_size=MEAN_VS_ODE_SAMPLE_SIZE,
        init_t=LOGISTIC_SIMULATION_START_TIME,
        sim_t=LOGISTIC_SIMULATION_RUN_TIME,
        init_st=int(CAPACITY / 10),
        params=(BASE_DOUBLING_TIME, CAPACITY),
        min_st=-25,
        max_st=225,
        shade_nonphysical=True,
        pdf_path=os.path.join(FIGURES, "logistic_growth_mean_vs_ode.pdf"),
        width_frac=0.7, display_frac=1.0, aspect=0.7 * 0.75,
    )
