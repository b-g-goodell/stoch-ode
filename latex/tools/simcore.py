from random import random
from math import log

MAX_ATTEMPTS = 10000


def rates_to_pmf(rates):
    if not rates:
        raise ValueError('No event rates supplied.')
    if any(rate < 0 for rate in rates):
        raise ValueError('Rates must be non-negative.')
    total_rate = sum(rates)
    if total_rate == 0.0:
        return None, 0.0  # absorbing state
    pmf = [rate/total_rate for rate in rates]
    pmf[-1] = max(0.0, 1.0 - sum(pmf[:-1]))
    return pmf, total_rate


def pmf_to_event_index(pmf):
    if not all(0.0 <= p <= 1.0 for p in pmf):
        raise ValueError('PMF must consist of probabilities.')
    elif abs(sum(pmf) - 1.0) > 1e-9:
        raise ValueError('PMF must sum to 1.0.')
    u = 1.0 - random()  # 0.0 < u <= 1.0
    sampled_index = 0
    next_cdf_value = pmf[sampled_index]
    while (next_cdf_value < u or pmf[sampled_index] == 0.0) and sampled_index < len(pmf)-1:
        sampled_index += 1
        next_cdf_value += pmf[sampled_index]
    return sampled_index


def rate_to_delta_time(rate):
    if rate <= 0.0:
        raise ValueError('Rate must be positive.')
    v = 1.0 - random()  # 0.0 < v <= 1.0
    return -log(v)/rate


def find_traj(init_t, sim_t, init_st, params, sim_func, succ_func):
    num_attempts = 0
    trajectory = sim_func((init_t, sim_t, init_st, params))
    num_attempts += 1
    while not succ_func(trajectory) and num_attempts < MAX_ATTEMPTS:
        trajectory = sim_func((init_t, sim_t, init_st, params))
        num_attempts += 1
    return trajectory, num_attempts
