"""Tests for src/recording.py: a valid recording passes, bad ones are refused."""

import numpy as np
import pytest

from src.recording import Recording


def make_valid_recording() -> Recording:
    """A small, well-formed recording used as the starting point in each test."""
    # 2 channels, 100 samples, sampled at 250 Hz.
    data = np.zeros((2, 100), dtype=float)
    events = [(10, "standard"), (40, "target"), (70, "distractor")]
    return Recording(
        data=data,
        sfreq=250.0,
        ch_names=["Pz", "Cz"],
        events=events,
        source="simulated",
        subject_id="S001",
    )


def test_valid_recording_passes():
    """A correctly shaped recording with good events validates without error."""
    recording = make_valid_recording()
    assert recording.validate() is None
    # The brief says is_simulated defaults to False.
    assert recording.is_simulated is False


def test_wrong_channel_count_fails():
    """Two rows of data but three channel names is refused."""
    recording = make_valid_recording()
    recording.ch_names = ["Pz", "Cz", "Fz"]
    with pytest.raises(ValueError, match="ch_names"):
        recording.validate()


def test_bad_label_fails():
    """An event label outside standard/target/distractor is refused."""
    recording = make_valid_recording()
    recording.events = [(10, "blink")]
    with pytest.raises(ValueError, match="not allowed"):
        recording.validate()


def test_event_past_end_fails():
    """An event sample index beyond the last sample is refused."""
    recording = make_valid_recording()
    recording.events = [(100, "target")]  # valid indices stop at 99
    with pytest.raises(ValueError, match="past the last sample"):
        recording.validate()


def test_negative_event_index_fails():
    """An event sample index below zero is refused."""
    recording = make_valid_recording()
    recording.events = [(-1, "target")]
    with pytest.raises(ValueError, match="negative"):
        recording.validate()


def test_not_two_dimensional_fails():
    """A flat (1-D) data array is refused."""
    recording = make_valid_recording()
    recording.data = np.zeros(100, dtype=float)
    with pytest.raises(ValueError, match="2-dimensional"):
        recording.validate()
