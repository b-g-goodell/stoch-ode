# Spec: each plotter owns its page styling. Given width_frac, display_frac, aspect,
# it sets matplotlib rcParams before drawing. Scripts pass these numbers and hold
# no rcParams logic. Behavior -> test:
#   figure size from width_frac and aspect          -> test_figsize_from_width_and_aspect
#   text size scales by width_frac/display_frac      -> test_font_size_scales_with_ratio
#   streamplot arrow scales by width_frac/display    -> test_arrowsize_scales_with_ratio

import pytest
from matplotlib import pyplot

import tools.plots.plot_trajectories as pt
import tools.plots.plot_vector_field as pvf

TRAJ = [[(0.0, 0.0), (1.0, 1.0)]]
TEXTWIDTH_IN = 354.12 / 72.27  # SIAMbook2019 \textwidth in inches


def test_figsize_from_width_and_aspect():
    pt.plot_trajs(0.0, 1.0, 0.0, 1.0, TRAJ, "t", "x", "y",
                  width_frac=0.5, display_frac=1.0, aspect=0.6)
    width = 0.5 * TEXTWIDTH_IN
    assert list(pyplot.rcParams["figure.figsize"]) == pytest.approx([width, width * 0.6])


def test_font_size_scales_with_ratio():
    pt.plot_trajs(0.0, 1.0, 0.0, 1.0, TRAJ, "t", "x", "y",
                  width_frac=1.0, display_frac=0.5, aspect=0.75)
    assert pyplot.rcParams["font.size"] == pytest.approx(9 * (1.0 / 0.5))


def test_arrowsize_scales_with_ratio(monkeypatch):
    captured = {}
    monkeypatch.setattr(pyplot, "streamplot", lambda *a, **k: captured.update(k))
    pvf.make_phase_diagram(0.5, 0.0, 1.0, 0.0, 10.0, "t", "x", "y",
                           lambda a: -a[0] * a[2],
                           width_frac=0.7, display_frac=1.0)
    assert captured["arrowsize"] == pytest.approx(0.48 * (0.7 / 1.0))
