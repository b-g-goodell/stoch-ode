import functools

import matplotlib

matplotlib.use("Agg")  # must run before pyplot is imported

import pytest
from matplotlib import pyplot


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: statistical tests, deselected by default"
    )
    config.addinivalue_line(
        "markers", "statistical: empirical-distribution checks with tolerances"
    )


@pytest.fixture(autouse=True)
def no_show(monkeypatch):
    """Neutralize pyplot.show and close figures around every test."""
    monkeypatch.setattr(pyplot, "show", lambda *a, **k: None)
    pyplot.close("all")
    yield
    pyplot.close("all")


@pytest.fixture(autouse=True)
def no_latex(monkeypatch):
    """Keep plot styling deterministic and independent of a system latex install."""
    monkeypatch.setattr("shutil.which", lambda name: None)


def install_fixed_uniform(monkeypatch, values):
    iterator = iter(values)
    monkeypatch.setattr("tools.simcore.random", lambda: next(iterator))


@pytest.fixture
def fixed_uniform(monkeypatch):
    """Drive tools.simcore.random() from an explicit sequence of values."""
    return functools.partial(install_fixed_uniform, monkeypatch)


@pytest.fixture
def seeded():
    """Seed the shared generator for reproducible statistical tests."""
    import random
    random.seed(20240601)
    yield


@pytest.fixture
def import_radioactive():
    """Return the radioactive_decay script module."""
    import scripts.radioactive_decay as rd
    return rd
