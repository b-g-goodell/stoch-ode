from tools.simcore import rates_to_pmf, pmf_to_event_index, rate_to_delta_time, find_traj
from tools.plots.plot_trajectories import plot_trajs
from tools.plots.plot_heatmap_histogram import plot_heatmap
from math import log, ceil

HEATMAP_SAMPLE_SIZE = 128


def make_allee_rates(state, base_doubling_time, coop_thresh, capacity):
    base_birth_rate = log(2) / base_doubling_time
    death_rate_0 = base_birth_rate * state
    birth_rate_0 = base_birth_rate * state**2 / capacity
    birth_rate_1 = base_birth_rate * state**2 / coop_thresh
    death_rate_1 = base_birth_rate * state**3 / (capacity * coop_thresh)
    return [death_rate_0, birth_rate_0, birth_rate_1, death_rate_1]


def make_allee_delta_states(params):
    return [-1, 1, 1, -1]


def dg_simulate_allee_ode(initial_time, simulation_run_time, initial_state, params):
    base_dbl_t, coop_thresh, capacity = params
    t = initial_time
    state = initial_state
    trajectory = [(t, state)]
    delta_states = make_allee_delta_states(params)
    while t < simulation_run_time and state > 0:
        rates = make_allee_rates(state, base_dbl_t, coop_thresh, capacity)
        pmf, total_rate = rates_to_pmf(rates=rates)
        delta_time = rate_to_delta_time(rate=total_rate)
        index = pmf_to_event_index(pmf=pmf)
        t += delta_time
        state += delta_states[index]
        trajectory.append((t, state))
    return trajectory


def plot_extinction_and_survival(init_t, sim_t, init_st, params, pdf_path=None,
                                 width_frac=1.0, display_frac=1.0, aspect=0.75):
    dbl_t, coop, cap = params
    sim_func = lambda x: dg_simulate_allee_ode(x[0], x[1], x[2], x[3])
    succ_func = lambda traj: traj[-1][1] == 0
    ext_traj, ext_ct = find_traj(init_t, sim_t, init_st, params, sim_func, succ_func)

    succ_func = lambda traj: traj[-1][1] >= cap
    succ_traj, succ_ct = find_traj(init_t, sim_t, init_st, params, sim_func, succ_func)

    min_t = init_t
    max_t = min(ext_traj[-1][0], succ_traj[-1][0], sim_t)
    min_st = 0
    max_st = ceil(max(succ_traj[i][1] for i in range(len(succ_traj)))*11/9)
    title = 'Simulated Populations with Allee Effect'
    xlabel = 'Time'
    ylabel = 'Population'
    plot_kwargs = dict(min_t=min_t, max_t=max_t, min_st=min_st, max_st=max_st,
                       trajs=[ext_traj, succ_traj], title=title, xlabel=xlabel, ylabel=ylabel)
    plot_trajs(**plot_kwargs, save_path=pdf_path,
               width_frac=width_frac, display_frac=display_frac, aspect=aspect)


def generate_allee_heatmap(init_t, sim_t, init_st, params, sample_size=HEATMAP_SAMPLE_SIZE,
                            pdf_path=None, width_frac=1.0, display_frac=1.0, aspect=0.75):
    base_dbl_t, coop, cap = params
    sim_trajs = []
    sim_func = lambda x: dg_simulate_allee_ode(x[0], x[1], x[2], x[3])
    succ_func = lambda traj: len(traj) > 0
    ext_ct = 0
    survive_ct = 0
    for _ in range(sample_size):
        traj, ct = find_traj(init_t, sim_t, init_st, params, sim_func, succ_func)
        if traj[-1][1] == 0:
            ext_ct += 1
        else:
            survive_ct += 1
        sim_trajs.append(traj)

    title = 'Simulated Populations with Allee Effect'
    xlabel = 'Time'
    ylabel = 'Population'
    plot_heatmap(sim_trajs, sim_t, title, xlabel, ylabel, save_path=pdf_path,
                 width_frac=width_frac, display_frac=display_frac, aspect=aspect)
