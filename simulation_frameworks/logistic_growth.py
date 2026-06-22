from tools.plots.plot_vector_field import make_phase_diagram
from tools.simcore import rates_to_pmf, pmf_to_event_index, rate_to_delta_time
from math import log, exp


LOGISTIC_SAMPLE_SIZE = 100
MEAN_VS_ODE_SAMPLE_SIZE = 30
MEAN_VS_ODE_GRID_POINTS = 500
LOGISTIC_SIMULATION_START_TIME = 0.0
LOGISTIC_SIMULATION_RUN_TIME = 365.0
BASE_DOUBLING_TIME = 36.5
CAPACITY = 200.0
PARAMETER_SPACE_EXPLORATION_RESOLUTION = 5j


def log_growth_phase(base_dbl_t, capacity, min_t_per_dbl_t, max_t_per_dbl_t, min_pop, max_pop,
                     pdf_path=None, shade_nonphysical=False, width_frac=1.0, display_frac=1.0, aspect=0.75,
                     xlabel='Time', ylabel='Population/Carrying Capacity'):
    base_birth_rate = log(2) / base_dbl_t
    params = (base_birth_rate, capacity)
    title = 'Logistic Growth ODE Solutions'
    min_time = min_t_per_dbl_t * base_dbl_t
    max_time = max_t_per_dbl_t * base_dbl_t
    dydt = lambda args: args[0][0] * args[2] * (1 - args[2] / args[0][1])
    make_phase_diagram(params, min_time, max_time, min_pop, max_pop, title, xlabel, ylabel, dydt,
                       save_path=pdf_path, shade_nonphysical=shade_nonphysical, width_frac=width_frac, display_frac=display_frac, aspect=aspect)


def make_logistic_rates(state, base_doubling_time, capacity):
    base_birth_rate = log(2) / base_doubling_time
    birth_rate = base_birth_rate * state
    death_rate = base_birth_rate * state**2 / capacity
    return [birth_rate, death_rate]


def make_logistic_delta_states(params):
    return [1, -1]


def state_at_time(traj, t):
    state = traj[0][1]
    for tj, sj in traj:
        if tj <= t:
            state = sj
        else:
            break
    return state


def compute_mean_trajectory(trajs, time_grid):
    n = len(trajs)
    return [(t, sum(state_at_time(traj, t) for traj in trajs) / n) for t in time_grid]


def logistic_ode_solution(P0, r, K, time_grid):
    # Exact particular solution to dP/dt = rP(1 - P/K) with P(0) = P0.
    return [(t, K * P0 / (P0 + (K - P0) * exp(-r * t))) for t in time_grid]


def log_growth_mean_vs_ode(sample_size, init_t, sim_t, init_st, params,
                            n_grid=MEAN_VS_ODE_GRID_POINTS,
                            min_st=0, max_st=None, shade_nonphysical=False,
                            pdf_path=None, width_frac=1.0, display_frac=1.0, aspect=0.75):
    from tools.plots.plot_mean_vs_ode import plot_mean_vs_ode
    base_dbl_t, capacity = params
    r = log(2) / base_dbl_t
    if max_st is None:
        max_st = int(capacity * 1.1)
    trajs = [dg_simulate_logistic_ode(init_t, sim_t, init_st, params)
             for _ in range(sample_size)]
    time_grid = [init_t + (sim_t - init_t) * i / (n_grid - 1) for i in range(n_grid)]
    mean_traj = compute_mean_trajectory(trajs, time_grid)
    ode_traj = logistic_ode_solution(init_st, r, capacity, time_grid)
    _, mean_states = zip(*mean_traj)
    _, ode_states = zip(*ode_traj)
    kwargs = dict(
        time_grid=time_grid,
        mean_states=list(mean_states),
        ode_states=list(ode_states),
        min_st=min_st,
        max_st=max_st,
        shade_nonphysical=shade_nonphysical,
        title='Logistic Growth: Stochastic Mean vs. ODE Solution',
        xlabel='Time (days)',
        ylabel='Population',
    )
    plot_mean_vs_ode(**kwargs, save_path=pdf_path,
                     width_frac=width_frac, display_frac=display_frac, aspect=aspect)


def dg_simulate_logistic_ode(initial_time, simulation_run_time, initial_state, params):
    base_doubling_time, capacity = params
    t = initial_time
    state = initial_state
    trajectory = [(t, state)]
    delta_states = make_logistic_delta_states(params)
    while t < simulation_run_time and state > 0:
        rates = make_logistic_rates(state=state, base_doubling_time=base_doubling_time,
                                    capacity=capacity)
        pmf, total_rate = rates_to_pmf(rates=rates)
        delta_time = rate_to_delta_time(rate=total_rate)
        index = pmf_to_event_index(pmf=pmf)
        t += delta_time
        state += delta_states[index]
        trajectory.append((t, state))
    return trajectory
