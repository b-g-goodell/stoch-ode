import os
import shutil
from matplotlib import pyplot
from numpy import mgrid, ones_like


def make_phase_diagram(params, min_t, max_t, min_y, max_y, title, xlabel, ylabel,
                       y_len_fun, res=100j,
                       width_frac=1.0, display_frac=1.0, aspect=0.75,
                       save_path=None, shade_nonphysical=False):
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

    y_pts, t_pts = mgrid[min_y:max_y:res, min_t:max_t:res]
    t_arr_len = ones_like(t_pts)
    y_arr_len = y_len_fun((params, t_pts, y_pts))

    pyplot.streamplot(t_pts, y_pts, t_arr_len, y_arr_len, density=(0.5, 1.0),
                      color='blue', arrowsize=0.48 * scale)
    if shade_nonphysical and min_y < 0:
        pyplot.axhspan(min_y, min(0.0, max_y), color='red', alpha=0.5, zorder=0)
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
