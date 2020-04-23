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
"""JAX Schedules.

Schedules may be used to anneal the value of a hyper-parameter over time; for
instance, they may be used to anneal the learning rate used to update an agent's
parameters or the exploration factor used to select actions.
"""

import jax.numpy as jnp
from rlax._src import base


Scalar = base.Scalar


def polynomial_schedule(
    init_value: Scalar,
    end_value: Scalar,
    power: Scalar,
    transition_steps: int,
    transition_begin: int = 0):
  """Construct a schedule with polynomial transition from init to end value."""
  if transition_steps < 0:
    raise ValueError('transition_steps must be a non-negative integer.')

  elif transition_steps == 0:
    return lambda step_count: end_value

  else:
    def schedule(step_count):
      count = jnp.clip(step_count - transition_begin, 0, transition_steps)
      frac = 1 - count / transition_steps
      return (init_value - end_value) * (frac**power) + end_value
    return schedule
