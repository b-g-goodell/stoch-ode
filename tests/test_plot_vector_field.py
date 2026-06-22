import numpy as np
from matplotlib import pyplot

import tools.plots.plot_vector_field as pvf


class TestMakePhaseDiagram:
    def test_grid_shape_and_constant_time_component(self, monkeypatch):
        captured = {}
        monkeypatch.setattr(pyplot, "streamplot",
                            lambda *a, **k: captured.update(args=a))
        pvf.make_phase_diagram(0.5, 0.0, 1.0, 0.0, 10.0, "t", "x", "y",
                               lambda a: -a[0] * a[2])
        t_pts, y_pts, t_arr_len, _ = captured["args"][:4]
        assert t_pts.shape == (100, 100)
        assert y_pts.shape == (100, 100)
        assert t_arr_len.shape == (100, 100)
        assert np.allclose(t_arr_len, 1.0)

    def test_field_values_match_supplied_function(self, monkeypatch):
        captured = {}
        monkeypatch.setattr(pyplot, "streamplot",
                            lambda *a, **k: captured.update(args=a))
        rate = 0.5
        pvf.make_phase_diagram(rate, 0.0, 1.0, 0.0, 10.0, "t", "x", "y",
                               lambda a: -a[0] * a[2])
        _, y_pts, _, y_arr_len = captured["args"][:4]
        assert np.allclose(y_arr_len, -rate * y_pts)

    def test_delegates_to_pyplot(self, monkeypatch):
        calls = {"streamplot": 0, "show": 0}
        monkeypatch.setattr(
            pyplot, "streamplot",
            lambda *a, **k: calls.__setitem__("streamplot", calls["streamplot"] + 1),
        )
        monkeypatch.setattr(
            pyplot, "show",
            lambda *a, **k: calls.__setitem__("show", calls["show"] + 1),
        )
        pvf.make_phase_diagram(0.5, 0.0, 1.0, 0.0, 10.0, "t", "x", "y",
                               lambda a: -a[0] * a[2])
        assert calls["streamplot"] == 1
        assert calls["show"] == 1
