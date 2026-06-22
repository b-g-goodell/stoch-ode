# Spec: each plot module is flattened to a single function, its plot_X entry
# point. No supporting functions remain at module level. Behavior -> test:
#   one function per module -> test_module_defines_exactly_one_function
import importlib
import inspect

import pytest


@pytest.mark.parametrize("module_name, func_name", [
    ("tools.plots.plot_trajectories", "plot_trajs"),
    ("tools.plots.plot_mean_vs_ode", "plot_mean_vs_ode"),
    ("tools.plots.plot_heatmap_histogram", "plot_heatmap"),
    ("tools.plots.plot_vector_field", "make_phase_diagram"),
])
def test_module_defines_exactly_one_function(module_name, func_name):
    module = importlib.import_module(module_name)
    defined = [name for name, obj in inspect.getmembers(module, inspect.isfunction)
               if obj.__module__ == module.__name__]
    assert defined == [func_name]
