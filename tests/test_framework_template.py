from functools import partial

import simulation_frameworks.framework_template as ft


def stub_collaborators(monkeypatch, *, delta_time=1.0, event_index=0,
                       rates=None, delta_state=1):
    rates = rates if rates is not None else [1.0]
    monkeypatch.setattr(ft, "make_rates", lambda state, params: list(rates))
    monkeypatch.setattr(ft, "rate_to_delta_time", lambda rate: delta_time)
    monkeypatch.setattr(ft, "make_delta_states", lambda params: [delta_state] * (event_index + 1))
    monkeypatch.setattr(ft, "pmf_to_event_index", lambda pmf: event_index)


def boom(*args, **kwargs):
    raise AssertionError("collaborator should not be called")


def record_call(order, name, ret, *args, **kwargs):
    order.append(name)
    return ret


class TestDgSimulateOde:
    def test_state_advances_by_delta_state_each_step(self, monkeypatch):
        stub_collaborators(monkeypatch, delta_time=1.0, delta_state=1)
        traj = ft.dg_simulate_ode(0, 2.5, 5, None)
        assert traj == [(0, 5), (1.0, 6), (2.0, 7), (3.0, 8)]

    def test_loop_stops_when_total_rate_is_zero(self, monkeypatch):
        rate_seq = iter([([1.0], 1.0), ([1.0], 1.0), ([1.0], 0.0)])
        stub_collaborators(monkeypatch, delta_time=1.0, delta_state=-1)
        monkeypatch.setattr(ft, "rates_to_pmf", lambda rates: next(rate_seq))
        traj = ft.dg_simulate_ode(0, 100.0, 2, None)
        assert traj == [(0, 2), (1.0, 1), (2.0, 0)]

    def test_loop_is_strict_less_than_run_time(self, monkeypatch):
        monkeypatch.setattr(ft, "make_rates", boom)
        traj = ft.dg_simulate_ode(5, 5, 3, None)
        assert traj == [(5, 3)]

    def test_collaborator_call_order_within_one_iteration(self, monkeypatch):
        order = []
        for name, ret in [
            ("make_delta_states", [1]),
            ("make_rates", [1.0]),
            ("rates_to_pmf", ([1.0], 1.0)),
            ("rate_to_delta_time", 1.0),
            ("pmf_to_event_index", 0),
        ]:
            monkeypatch.setattr(ft, name, partial(record_call, order, name, ret))
        ft.dg_simulate_ode(0.0, 0.5, 1, None)
        assert order == [
            "make_delta_states",
            "make_rates",
            "rates_to_pmf",
            "rate_to_delta_time",
            "pmf_to_event_index",
        ]
