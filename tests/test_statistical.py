import math

import pytest

from tools.simcore import rate_to_delta_time, pmf_to_event_index

pytestmark = pytest.mark.slow


def test_delta_time_mean_matches_inverse_rate(seeded):
    rate = 2.0
    n = 40000
    samples = [rate_to_delta_time(rate) for _ in range(n)]
    mean = sum(samples) / n
    standard_error = (1.0 / rate) / math.sqrt(n)
    assert abs(mean - 1.0 / rate) < 5 * standard_error


def test_event_frequencies_match_pmf(seeded):
    pmf = [0.2, 0.3, 0.5]
    n = 60000
    counts = [0, 0, 0]
    for _ in range(n):
        counts[pmf_to_event_index(pmf)] += 1
    for i, p in enumerate(pmf):
        assert abs(counts[i] / n - p) < 0.02
