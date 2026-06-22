import math

import pytest


class TestRadDecayPhase:
    def test_base_rate_and_time_window(self, import_radioactive, monkeypatch):
        rd = import_radioactive
        captured = {}
        monkeypatch.setattr(rd, "make_phase_diagram",
                            lambda *a, **k: captured.update(args=a))
        rd.rad_decay_phase(half_life=2.0, min_t_per_hl=0.0, max_t_per_hl=3.0,
                           min_mass=0.0, max_mass=10.0)
        assert captured["args"][0] == pytest.approx([math.log(2) / 2.0])
        assert captured["args"][1] == pytest.approx(0.0)
        assert captured["args"][2] == pytest.approx(6.0)

    def test_field_is_negative_rate_times_mass_and_ignores_time(
        self, import_radioactive, monkeypatch
    ):
        rd = import_radioactive
        captured = {}
        monkeypatch.setattr(
            rd, "make_phase_diagram",
            lambda *a, **k: captured.update(y_len_fun=a[8]),
        )
        rd.rad_decay_phase(1.0, 0.0, 1.0, 0.0, 10.0)
        field = captured["y_len_fun"]
        rate, mass = 0.35, 10.0
        assert field(([rate], 0.0, mass)) == pytest.approx(-rate * mass)
        # dy/dt does not depend on t:
        assert field(([rate], 99.0, mass)) == field(([rate], -7.0, mass))

    def test_zero_half_life_raises(self, import_radioactive):
        rd = import_radioactive
        with pytest.raises(ZeroDivisionError):
            rd.rad_decay_phase(0, -0.5, 5, -10, 80)
