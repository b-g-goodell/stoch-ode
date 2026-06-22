from tools.simcore import rates_to_pmf, pmf_to_event_index, rate_to_delta_time, find_traj

SAMPLE_SIZE = 100000
INIT_TIME = 0.0
SIM_TIME = 1000.0
CLEAN_IN = 100.0
SALTY_IN = 100.0
VOL = 1.0e6
CONC = 2.9112e-26  # hand-tuned for nice-looking graphs
INIT_STATE = 300
TOO_MANY_MOLECULES = 310
SALT_MASS = 9.704e-23  # kg per molecule

PARAMS = CLEAN_IN, SALTY_IN, CONC, VOL, SALT_MASS


def make_tank_rates(state, clean_in, salty_in, conc, vol, mass):
    salt_arrival_rate = salty_in * conc / mass
    salt_departure_rate = (clean_in + salty_in) * state / vol
    return [salt_arrival_rate, salt_departure_rate]


def make_tank_delta_states(params):
    return [1, -1]


def dg_simulate_tank_ode(initial_time=INIT_TIME, simulation_run_time=SIM_TIME, initial_state=INIT_STATE, params=PARAMS):
    clean_in, salty_in, conc, vol, mass = params
    t = initial_time
    state = initial_state
    traj = [(t, state)]
    delta_states = make_tank_delta_states(params)
    # M = 0 is not absorbing: arrivals continue.
    while t < simulation_run_time:
        rates = make_tank_rates(state, clean_in, salty_in, conc, vol, mass)
        pmf, total_rate = rates_to_pmf(rates=rates)
        delta_time = rate_to_delta_time(rate=total_rate)
        index = pmf_to_event_index(pmf=pmf)
        t += delta_time
        state += delta_states[index]
        traj.append((t, state))
    return traj


def est_too_many(initial_time, simulation_run_time, initial_state, params):
    exceed = 0
    for _ in range(SAMPLE_SIZE):
        traj = dg_simulate_tank_ode(
            initial_time, simulation_run_time, initial_state, params)
        if any(state > TOO_MANY_MOLECULES for _, state in traj):
            exceed += 1
    return exceed / SAMPLE_SIZE
