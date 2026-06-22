# Spec: the four plotter modules live under tools.plots and expose their public
# entry points unchanged. Behavior -> test:
#   import paths resolve from tools.plots -> test_public_plotters_importable
import importlib

import pytest


@pytest.mark.parametrize("module_name, attr", [
    ("tools.plots.plot_trajectories", "plot_trajs"),
    ("tools.plots.plot_mean_vs_ode", "plot_mean_vs_ode"),
    ("tools.plots.plot_heatmap_histogram", "plot_heatmap"),
    ("tools.plots.plot_vector_field", "make_phase_diagram"),
])
def test_public_plotters_importable(module_name, attr):
    module = importlib.import_module(module_name)
    assert hasattr(module, attr)
