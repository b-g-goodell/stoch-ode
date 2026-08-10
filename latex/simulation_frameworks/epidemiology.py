from tools.simcore import rates_to_pmf, pmf_to_event_index, rate_to_delta_time
from tools.plots.plot_trajectories import plot_trajs
from math import log

SIR_SIMULATION_START_TIME = 0.0
SIR_SIMULATION_RUN_TIME = 365.0
TIME_BETWEEN_INTERACTIONS = 0.001
RECOVERY_HALF_LIFE = 45.0
INFECTION_PROBABILITY = 0.0001
INITIAL_SIR_STATE = [90, 10, 0]


def make_sir_rates(state, time_between_interactions, recovery_half_life,
                   infection_probability):
    total_population = sum(state)
    transmissibility = infection_probability / (
        time_between_interactions * total_population)
    per_capita_recovery_rate = log(2) / recovery_half_life
    susceptibles, infectious, _ = state
    return [transmissibility * susceptibles * infectious,
            per_capita_recovery_rate * infectious]


def make_sir_delta_states(params):
    return [[-1, 1, 0], [0, -1, 1]]


def update_sir_state(state, delta_state):
    return [s + d for s, d in zip(state, delta_state)]


def dg_simulate_sir_ode(initial_time, simulation_run_time, initial_state, params):
    time_between_interactions, recovery_half_life, infection_probability = params
    t = initial_time
    state = initial_state
    trajectory = [(t, state)]
    delta_states = make_sir_delta_states(params)
    while t < simulation_run_time and state[1] > 0 and sum(state) > 0:
        rates = make_sir_rates(state=state,
                               time_between_interactions=time_between_interactions,
                               recovery_half_life=recovery_half_life,
                               infection_probability=infection_probability)
        pmf, time_rate = rates_to_pmf(rates=rates)
        delta_time = rate_to_delta_time(rate=time_rate)
        index = pmf_to_event_index(pmf=pmf)
        t += delta_time
        state = update_sir_state(state=state, delta_state=delta_states[index])
        trajectory.append((t, state))
    return trajectory


def simulate_and_plot(initial_time, simulation_run_time, initial_state, params,
                      pdf_path=None, width_frac=1.0, display_frac=1.0, aspect=0.75):
    stochastic_trajectory = dg_simulate_sir_ode(initial_time=initial_time,
                                                simulation_run_time=simulation_run_time,
                                                initial_state=initial_state,
                                                params=params)
    susceptible_trajectory = []
    infectious_trajectory = []
    resistant_trajectory = []
    max_time = stochastic_trajectory[-1][0]
    for next_time, next_state in stochastic_trajectory:
        susceptible_trajectory.append((next_time, next_state[0]))
        infectious_trajectory.append((next_time, next_state[1]))
        resistant_trajectory.append((next_time, next_state[2]))

    trajs = [susceptible_trajectory, infectious_trajectory, resistant_trajectory]
    plot_kwargs = dict(min_t=initial_time, max_t=max_time, min_st=0, max_st=sum(initial_state),
                       trajs=trajs, title='Simulated Disease Progression from SIR Model',
                       xlabel='Time', ylabel='Subpopulation count', labels=['S', 'I', 'R'])
    plot_trajs(**plot_kwargs, save_path=pdf_path,
               width_frac=width_frac, display_frac=display_frac, aspect=aspect)
