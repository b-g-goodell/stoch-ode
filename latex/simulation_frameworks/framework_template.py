from tools.simcore import rates_to_pmf, rate_to_delta_time, pmf_to_event_index

def make_rates(state, params):
    ...

def make_delta_states(params):
    ...

def dg_simulate_ode(init_t, sim_t, init_st, sys_pars):
    delta_states = make_delta_states(sys_pars) # step 1
    t, st, traj = init_t, init_st, [(init_t, init_st)] # step 2
    while t < sim_t:
        rates = make_rates(st, sys_pars) # step 3
        pmf, rate = rates_to_pmf(rates=rates) # step 4
        if rate == 0.0: # step 5
            break
        delta_t = rate_to_delta_time(rate=rate) # step 6
        index_j = pmf_to_event_index(pmf=pmf) # step 7
        t, st = t+delta_t, st+delta_states[index_j] # step 8
        traj = traj + [(t, st)]
    return traj
