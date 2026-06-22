import os
import shutil
from matplotlib import pyplot
from numpy import linspace, array, searchsorted, clip, concatenate, tile, histogram2d, percentile


def plot_heatmap(trajectories, simulation_run_time, title, xlabel, ylabel,
                 grid=16, save_path=None,
                 width_frac=1.0, display_frac=1.0, aspect=0.75):
    textwidth_in = 354.12 / 72.27  # SIAMbook2019 \textwidth in inches
    scale = width_frac / display_frac
    on_page_pt = (10 - 1) * scale
    width = width_frac * textwidth_in
    text_keys = ('font.size', 'axes.titlesize', 'axes.labelsize',
                 'xtick.labelsize', 'ytick.labelsize', 'legend.fontsize')
    rc = {key: on_page_pt for key in text_keys}
    rc.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'figure.dpi': 150,
        'figure.figsize': (width, width * aspect),
        'lines.linewidth': 1.5 * 0.48 * scale,
    })
    if shutil.which('latex') is not None:
        rc['text.usetex'] = True
        rc['text.latex.preamble'] = r'\usepackage{times}\usepackage{mathptmx}'
    pyplot.rcParams.update(rc)

    # sample every trajectory at center of gridded bins
    edges = linspace(0.0, simulation_run_time, grid + 1)
    sample_times = 0.5 * (edges[:-1] + edges[1:])
    sampled = []
    for trajectory in trajectories:
        times, states = zip(*trajectory)
        times, states = array(times), array(states)
        # index of the most recent change point
        held_index = clip(searchsorted(times, sample_times, side='right') - 1, 0, len(states) - 1)
        sampled.append(states[held_index])
    sampled_states = concatenate(sampled)
    sampled_times = tile(sample_times, len(trajectories))

    counts, t_edges, y_edges = histogram2d(
        sampled_times, sampled_states, bins=(grid, grid),
        range=[[0.0, simulation_run_time], [sampled_states.min(), sampled_states.max()]])

    # cap the brightest 5 percent of cells
    brightness_cap = percentile(counts, 95.0)
    image = pyplot.imshow(counts.T, origin='lower', aspect='auto',
                          extent=[t_edges[0], t_edges[-1], y_edges[0], y_edges[-1]],
                          vmin=0.0, vmax=brightness_cap,
                          cmap='magma', interpolation='bilinear', rasterized=True)
    bar = pyplot.colorbar(image)
    bar.set_ticks([0.0, brightness_cap])
    bar.set_ticklabels(['Few', 'Many'])
    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.tight_layout()
    if save_path is not None:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        pyplot.savefig(save_path, bbox_inches='tight')
        pyplot.close()
    else:
        pyplot.show()
