"""Tests for adaptive (auto-apply) sensor calibration (v2.7).

Covers the two pure functions that drive enable_auto_calibration:
  - update_calibration_bias: folds one (local, regional-reference) sample
    into a slow EMA of the residual bias per field.
  - compute_auto_calibration_step: turns a confident, persistent bias into
    a small, bounded, sign-correct nudge - or nothing, if unconfident or
    within the noise deadband.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from custom_components.ws_core.learning_state import (
    LearningState,
    compute_auto_calibration_step,
    update_calibration_bias,
)

DEADBAND = {"cal_temp_c": 0.3, "cal_humidity": 2.0, "cal_pressure_hpa": 1.0}
STEP = {"cal_temp_c": 0.1, "cal_humidity": 0.5, "cal_pressure_hpa": 0.2}


class TestUpdateCalibrationBias:
    def test_first_sample_sets_bias_to_the_delta(self):
        s = LearningState()
        update_calibration_bias(s, 21.0, 20.0, 55.0, 50.0, 1013.0, 1010.0, alpha=0.5)
        assert s.cal_bias_temp_c == 1.0
        assert s.cal_bias_humidity == 5.0
        assert s.cal_bias_pressure_hpa == 3.0
        assert s.cal_bias_n == 1

    def test_ema_moves_toward_new_sample_without_jumping_to_it(self):
        s = LearningState(cal_bias_temp_c=1.0, cal_bias_n=50)
        update_calibration_bias(s, 22.0, 20.0, None, None, None, None, alpha=0.1)
        # alpha=0.1: 0.1*2.0 + 0.9*1.0 = 1.1 - moved toward 2.0, but nowhere close to it.
        assert 1.0 < s.cal_bias_temp_c < 1.2
        assert s.cal_bias_n == 51

    def test_missing_local_or_reference_value_skips_that_field_only(self):
        s = LearningState()
        update_calibration_bias(s, None, 20.0, 55.0, 50.0, None, None, alpha=0.5)
        assert s.cal_bias_temp_c is None  # local missing
        assert s.cal_bias_humidity == 5.0
        assert s.cal_bias_pressure_hpa is None  # both missing
        assert s.cal_bias_n == 1  # still counted - at least one field updated

    def test_no_usable_field_does_not_increment_sample_count(self):
        s = LearningState()
        update_calibration_bias(s, None, 20.0, None, 50.0, None, None, alpha=0.5)
        assert s.cal_bias_n == 0


class TestComputeAutoCalibrationStep:
    def _state(self, **kw) -> LearningState:
        s = LearningState()
        for k, v in kw.items():
            setattr(s, k, v)
        return s

    def test_not_enough_samples_returns_nothing(self):
        s = self._state(cal_bias_temp_c=5.0, cal_bias_n=10)
        assert compute_auto_calibration_step(s, 240, DEADBAND, STEP) == {}

    def test_bias_within_deadband_returns_nothing(self):
        s = self._state(cal_bias_temp_c=0.2, cal_bias_n=300)
        assert compute_auto_calibration_step(s, 240, DEADBAND, STEP) == {}

    def test_confident_bias_beyond_deadband_nudges_opposite_sign(self):
        # Sensor reads 2.0°C high vs. reference -> nudge cal_temp_c down.
        s = self._state(cal_bias_temp_c=2.0, cal_bias_n=300)
        deltas = compute_auto_calibration_step(s, 240, DEADBAND, STEP)
        assert deltas == {"cal_temp_c": -0.1}  # capped at STEP, not the full 2.0

    def test_negative_bias_nudges_positive(self):
        # Sensor reads 4% low on humidity (beyond the 2.0 deadband) -> nudge up.
        s = self._state(cal_bias_humidity=-4.0, cal_bias_n=300)
        deltas = compute_auto_calibration_step(s, 240, DEADBAND, STEP)
        assert deltas == {"cal_humidity": 0.5}

    def test_step_caps_a_large_bias(self):
        # With the real tuning constants, deadband < step for every field, so
        # a bias big enough to clear the deadband is always bigger than the
        # step too - the nudge is capped at STEP, never the full bias.
        s = self._state(cal_bias_pressure_hpa=5.0, cal_bias_n=300)
        deltas = compute_auto_calibration_step(s, 240, DEADBAND, STEP)
        assert deltas == {"cal_pressure_hpa": -0.2}  # capped at STEP, not -5.0

    def test_step_never_exceeds_a_bias_smaller_than_the_step_cap(self):
        # General correctness of the min(step, |bias|) cap, independent of the
        # real constants: with a deadband smaller than the step, a bias that
        # only just clears the deadband must not be overshot by the nudge.
        loose_deadband = {"cal_temp_c": 0.1, "cal_humidity": 0.1, "cal_pressure_hpa": 0.1}
        big_step = {"cal_temp_c": 5.0, "cal_humidity": 5.0, "cal_pressure_hpa": 5.0}
        s = self._state(cal_bias_temp_c=0.35, cal_bias_n=300)
        deltas = compute_auto_calibration_step(s, 240, loose_deadband, big_step)
        assert deltas == {"cal_temp_c": -0.35}  # bias itself is the binding constraint

    def test_multiple_fields_evaluated_independently(self):
        s = self._state(
            cal_bias_temp_c=2.0,  # beyond deadband
            cal_bias_humidity=0.5,  # within deadband
            cal_bias_pressure_hpa=-3.0,  # beyond deadband
            cal_bias_n=300,
        )
        deltas = compute_auto_calibration_step(s, 240, DEADBAND, STEP)
        assert deltas == {"cal_temp_c": -0.1, "cal_pressure_hpa": 0.2}

    def test_unset_bias_is_skipped(self):
        s = self._state(cal_bias_n=300)  # all biases still None
        assert compute_auto_calibration_step(s, 240, DEADBAND, STEP) == {}
