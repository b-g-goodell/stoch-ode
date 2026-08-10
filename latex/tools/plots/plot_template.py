# tools/plots/plot_template.py
# Shared structure for tools/plots plotters: style, draw, save or show.
import os
import shutil
from matplotlib import pyplot


def plot_template(title, xlabel, ylabel, save_path=None,
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

    ...  # draw the figure: each plotter supplies this block

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
