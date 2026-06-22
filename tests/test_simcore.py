import math
import random
from itertools import count

import pytest

from tools.simcore import (
    rates_to_pmf,
    pmf_to_event_index,
    rate_to_delta_time,
    find_traj,
)


class TestRatesToPmf:
    def test_two_rates_normalize(self):
        pmf, total = rates_to_pmf([3, 1])
        assert total == 4
        assert pmf == [0.75, 0.25]

    def test_last_entry_is_the_corrected_remainder(self):
        pmf, _ = rates_to_pmf([3, 1])
        assert pmf[-1] == 1.0 - sum(pmf[:-1])

    def test_single_rate(self):
        pmf, total = rates_to_pmf([5.0])
        assert total == 5.0
        assert pmf == [1.0]

    def test_three_equal_rates_sum_to_one_within_tolerance(self):
        pmf, total = rates_to_pmf([1.0, 1.0, 1.0])
        assert total == 3.0
        assert len(pmf) == 3
        assert abs(sum(pmf) - 1.0) < 1e-12

    def test_negative_rate_rejected(self):
        with pytest.raises(ValueError):
            rates_to_pmf([-1, 2])

    def test_all_zeros_returns_zero_total(self):
        pmf, total = rates_to_pmf([0.0, 0.0])
        assert total == 0.0
        assert pmf is None

    def test_empty_list_rejected(self):
        with pytest.raises(ValueError):
            rates_to_pmf([])

    def test_corrected_remainder_never_negative_from_rounding(self):
        rates = [570683901.2551241, 0.000324659196328229, 5.194909927543226e-10]
        pmf, _ = rates_to_pmf(rates)
        assert all(0.0 <= p <= 1.0 for p in pmf)
        assert pmf[-1] == 0.0


class TestPmfToEvent:
    def test_low_u_selects_first(self, fixed_uniform):
        fixed_uniform([0.90])
        assert pmf_to_event_index([0.25, 0.75]) == 0

    def test_high_u_selects_second(self, fixed_uniform):
        fixed_uniform([0.50])
        assert pmf_to_event_index([0.25, 0.75]) == 1

    def test_singleton_pmf_returns_zero(self, fixed_uniform):
        fixed_uniform([0.99])
        assert pmf_to_event_index([1.0]) == 0

    def test_boundary_u_at_cumulative_selects_that_index(self, fixed_uniform):
        fixed_uniform([0.5])
        assert pmf_to_event_index([0.2, 0.3, 0.5]) == 1

    def test_zero_probability_event_is_skipped(self, fixed_uniform):
        fixed_uniform([0.0])
        assert pmf_to_event_index([0.0, 1.0]) == 1

    def test_not_probabilities_rejected(self):
        with pytest.raises(ValueError):
            pmf_to_event_index([-0.1, 1.1])

    def test_sum_far_from_one_rejected(self):
        with pytest.raises(ValueError):
            pmf_to_event_index([0.2, 0.2])

    def test_sum_within_tolerance_accepted(self, fixed_uniform):
        fixed_uniform([0.75])
        pmf = [0.49999999995, 0.49999999995]
        assert abs(sum(pmf) - 1.0) < 1e-9
        assert pmf_to_event_index(pmf) == 0

    def test_no_indexerror_when_u_exceeds_accumulated_sum(self, fixed_uniform):
        pmf = [0.49999999995, 0.49999999995]
        fixed_uniform([0.0])
        assert pmf_to_event_index(pmf) == 1


class TestRateToDeltaTime:
    def test_known_value(self, fixed_uniform):
        fixed_uniform([0.5])
        assert rate_to_delta_time(2.0) == pytest.approx(math.log(2) / 2.0)

    def test_target_delta(self, fixed_uniform):
        fixed_uniform([1.0 - math.exp(-3.0)])
        assert rate_to_delta_time(1.0) == pytest.approx(3.0)

    def test_zero_rate_rejected(self):
        with pytest.raises(ValueError):
            rate_to_delta_time(0.0)

    def test_negative_rate_rejected(self):
        with pytest.raises(ValueError):
            rate_to_delta_time(-1.0)

    def test_draw_zero_gives_zero_delta_no_domain_error(self, fixed_uniform):
        fixed_uniform([0.0])
        assert rate_to_delta_time(2.0) == 0.0


class TestFindTraj:
    def test_succeeds_on_first_attempt(self):
        sim_func = lambda x: [(0, 5)]
        succ_func = lambda traj: True
        traj, attempts = find_traj(0, 3, 5, None, sim_func, succ_func)
        assert attempts == 1
        assert traj == [(0, 5)]

    def test_counts_attempts_until_predicate_holds(self):
        counter = count(1)
        sim_func = lambda x: [(0, next(counter))]
        succ_func = lambda traj: traj[-1][1] >= 3
        traj, attempts = find_traj(0, 3, 5, None, sim_func, succ_func)
        assert attempts == 3
        assert traj[-1][1] == 3

    def test_sim_func_receives_a_single_packed_tuple(self):
        seen = {}
        find_traj(0, 9, 7, ("p",), lambda x: seen.update(arg=x) or [(0, 1)], lambda traj: True)
        assert seen["arg"] == (0, 9, 7, ("p",))


class TestComposition:
    def test_pmf_from_rates_is_accepted_by_pmf_to_event_index(self, seeded):
        rng = random.Random(7)
        for _ in range(3000):
            n = rng.randint(2, 6)
            scale = rng.choice([1e-3, 1.0, 1e3])
            rates = [rng.random() * scale + 1e-12 for _ in range(n)]
            pmf, _ = rates_to_pmf(rates)
            index = pmf_to_event_index(pmf)
            assert 0 <= index < n
