# Lint as: python3
# Copyright 2019 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for schedules.py."""

from absl.testing import absltest
from absl.testing import parameterized

import numpy as np

from rlax._src import schedules
from rlax._src import test_util


@test_util.parameterize_variant()
class PolynomialTest(parameterized.TestCase):

  def test_linear(self, variant):
    """Check linear schedule."""
    # Get schedule function.
    schedule_fn = schedules.polynomial_schedule(10., 20., 1, 10)
    schedule_fn = variant(schedule_fn)
    # Test that generated values equal the expected schedule values.
    generated_vals = []
    for count in range(15):
      # Compute next value.
      generated_vals.append(schedule_fn(count))
    # Test output.
    expected_vals = np.array(list(range(10, 20)) + [20] * 5, dtype=np.float32)
    np.testing.assert_allclose(
        expected_vals, np.array(generated_vals), atol=1e-3)

  def test_zero_steps_schedule(self, variant):
    # Get schedule function.
    num_steps = 0
    initial_value = 10.
    final_value = 20.

    for num_steps in [-1, 0]:
      schedule_fn = schedules.polynomial_schedule(
          initial_value, final_value, 1, num_steps)
      schedule_fn = variant(schedule_fn)
      for count in range(15):
        np.testing.assert_allclose(schedule_fn(count), initial_value)

  def test_nonlinear(self, variant):
    """Check non-linear (quadratic) schedule."""
    # Get schedule function.
    schedule_fn = schedules.polynomial_schedule(25., 10., 2, 10)
    schedule_fn = variant(schedule_fn)
    # Test that generated values equal the expected schedule values.
    generated_vals = []
    for count in range(15):
      # Compute next value.
      generated_vals.append(schedule_fn(count))
    # Test output.
    expected_vals = np.array(
        [10. + 15. * (1.-n/10)**2 for n in range(10)] + [10] * 5,
        dtype=np.float32)
    np.testing.assert_allclose(
        expected_vals, np.array(generated_vals), atol=1e-3)

  def test_with_decay_begin(self, variant):
    """Check quadratic schedule with non-zero schedule begin."""
    # Get schedule function.
    schedule_fn = schedules.polynomial_schedule(
        30., 10., 2, 10, transition_begin=4)
    schedule_fn = variant(schedule_fn)
    # Test that generated values equal the expected schedule values.
    generated_vals = []
    for count in range(20):
      # Compute next value.
      generated_vals.append(schedule_fn(count))
    # Test output.
    expected_vals = np.array(
        [30.] * 4 + [10. + 20. * (1.-n/10)**2 for n in range(10)] + [10] * 6,
        dtype=np.float32)
    np.testing.assert_allclose(
        expected_vals, np.array(generated_vals), atol=1e-3)


@test_util.parameterize_variant()
class PiecewiseConstantTest(parameterized.TestCase):

  def test_positive(self, variant):
    """Check piecewise constant schedule of positive values."""
    # Get schedule function.
    schedule_fn = schedules.piecewise_constant_schedule(0.1, {3: 2., 6: 0.5})
    schedule_fn = variant(schedule_fn)
    # Test that generated values equal the expected schedule values.
    generated_vals = []
    for count in range(10):
      # Compute next value.
      generated_vals.append(schedule_fn(count))
    # Test output.
    expected_vals = np.array(
        [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1])
    np.testing.assert_allclose(
        expected_vals, np.array(generated_vals), atol=1e-3)

  def test_negative(self, variant):
    """Check piecewise constant schedule of negative values."""
    # Get schedule function.
    schedule_fn = schedules.piecewise_constant_schedule(-0.1, {3: 2., 6: 0.5})
    schedule_fn = variant(schedule_fn)
    # Test that generated values equal the expected schedule values.
    generated_vals = []
    for count in range(10):
      # Compute next value.
      generated_vals.append(schedule_fn(count))
    # Test output.
    expected_vals = -1 * np.array(
        [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1])
    np.testing.assert_allclose(
        expected_vals, np.array(generated_vals), atol=1e-3)


if __name__ == '__main__':
  absltest.main()
