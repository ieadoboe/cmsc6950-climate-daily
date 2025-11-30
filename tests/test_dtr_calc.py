"""Tests for Daily Temperature Range Functions"""

import pytest
import numpy as np
import pandas as pd
from src.dtr_calc import calculate_dtr


@pytest.mark.parametrize("t_min,t_max,expected", [
    (10.0, 20.0, 10.0),
    (15.0, 15.0, 0.0),
    (-5.0, 5.0, 10.0),
    (-20.0, -10.0, 10.0),
    (0.0, 5.0, 5.0),
])
def test_valid_scalar_dtr(t_min, t_max, expected):
    """Test DTR calculation for valid scalar inputs"""
    result = calculate_dtr(t_min=t_min, t_max=t_max)
    assert result == expected


@pytest.mark.parametrize("t_min,t_max", [
    (20.0, 10.0),
    (15.0, 5.0),
])
def test_invalid_scalar_raises_error(t_min, t_max):
    """Test invalid scalar inputs raise ValueError"""
    with pytest.raises(ValueError, match="t_min must be <= t_max"):
        calculate_dtr(t_min=t_min, t_max=t_max)


@pytest.mark.parametrize("t_min,t_max,expected", [
    (np.array([5.0, 10.0]), np.array([10.0, 15.0]), np.array([5.0, 5.0])),
    (np.array([-10.0, 0.0]), np.array([-5.0, 10.0]), np.array([5.0, 10.0])),
    (np.array([0.0]), np.array([5.0]), np.array([5.0])),
])
def test_valid_array_dtr(t_min, t_max, expected):
    """Test DTR calculation with valid numpy arrays"""
    result = calculate_dtr(t_min=t_min, t_max=t_max)
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize("t_min,t_max", [
    (np.array([5.0, 20.0]), np.array([10.0, 10.0])),
    (np.array([20.0, 5.0]), np.array([10.0, 10.0])),
])
def test_invalid_array_raises_error(t_min, t_max):
    """Test that invalid array inputs raise ValueError"""
    with pytest.raises(ValueError, match="t_min must be <= t_max for all entries"):  # noqa:E501
        calculate_dtr(t_min=t_min, t_max=t_max)


@pytest.mark.parametrize("t_min,t_max,expected", [
    (pd.Series([5.0, 10.0]), pd.Series([10.0, 15.0]), pd.Series([5.0, 5.0])),
    (pd.Series([-5.0, 0.0]), pd.Series([5.0, 10.0]), pd.Series([10.0, 10.0])),
])
def test_valid_series_dtr(t_min, t_max, expected):
    """Test DTR calculation with valid pandas Series"""
    result = calculate_dtr(t_min=t_min, t_max=t_max)
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize("t_min,t_max", [
    (pd.Series([5.0, 20.0]), pd.Series([10.0, 10.0])),
    (pd.Series([20.0, 5.0]), pd.Series([10.0, 10.0])),
])
def test_invalid_series_raises_error(t_min, t_max):
    """Test that invalid Series inputs raise ValueError"""
    with pytest.raises(ValueError, match="t_min must be <= t_max for all entries"):  # noqa:E501
        calculate_dtr(t_min=t_min, t_max=t_max)
