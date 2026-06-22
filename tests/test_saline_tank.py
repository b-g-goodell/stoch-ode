from math import exp

import pytest

import simulation_frameworks.saline_tank as saline
from tools.simcore import rates_to_pmf
from simulation_frameworks.saline_tank import (
    make_tank_rates,
    make_tank_delta_states,
    dg_simulate_tank_ode,
)


class TestMakeTankRates:
    def test_rate_formula(self):
        assert make_tank_rates(5, 100, 100, 1e-3, 1e3, 1.0) == pytest.approx([0.1, 1.0])

    def test_arrival_independent_of_state(self):
        a = make_tank_rates(5, 100, 100, 1e-3, 1e3, 1.0)[0]
        b = make_tank_rates(50, 100, 100, 1e-3, 1e3, 1.0)[0]
        assert a == b

    def test_departure_linear_in_state(self):
        small = make_tank_rates(5, 100, 100, 1e-3, 1e3, 1.0)[1]
        large = make_tank_rates(50, 100, 100, 1e-3, 1e3, 1.0)[1]
        assert large == pytest.approx(10 * small)


class TestMakeTankDeltaStates:
    def test_values(self):
        assert make_tank_delta_states(saline.PARAMS) == [1, -1]


class TestDgSimulateTankOde:
    def test_single_arrival_step_then_time_termination(self, fixed_uniform):
        fixed_uniform([1.0 - exp(-1.1), 0.99])
        traj = dg_simulate_tank_ode(
            initial_time=0, simulation_run_time=0.5, initial_state=5,
            params=(100, 100, 1e-3, 1e3, 1.0),
        )
        assert len(traj) == 2
        assert traj[0] == (0, 5)
        assert traj[-1][0] == pytest.approx(1.0)
        assert traj[-1][1] == 6


def test_est_too_many_runs(monkeypatch):
    monkeypatch.setattr(saline, "SAMPLE_SIZE", 3)
    monkeypatch.setattr(saline, "TOO_MANY_MOLECULES", 4)
    p = saline.est_too_many(0.0, 1.0, 5, saline.PARAMS)
    assert p == 1.0


def test_zero_state_gives_zero_departure_rate():
    assert make_tank_rates(0, 100, 100, 1e-3, 1e3, 1.0)[1] == 0.0


def test_zero_state_is_simulable():
    rates_to_pmf(make_tank_rates(0, 100, 100, 1e-3, 1e3, 1.0))
