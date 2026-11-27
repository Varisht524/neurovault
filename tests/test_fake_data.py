"""Tests for src/fake_data.py: both fake makers build the same shaped recording.

The fake makers are what demos and later stages use, so these tests pin down
the shape the rest of the app relies on, and check the same seed repeats.
"""

import numpy as np

from src.fake_data import (
    SOURCE_CLEAN,
    SOURCE_NOISY,
    make_clean_recording,
    make_noisy_recording,
)


def test_same_seed_gives_identical_data():
    """Two calls with seed 1 give exactly the same samples and events."""
    first = make_clean_recording(1)
    second = make_clean_recording(1)

    np.testing.assert_array_equal(first.data, second.data)
    assert first.events == second.events


def test_different_seeds_give_different_data():
    """A different seed must not repeat the same recording."""
    first = make_clean_recording(1)
    second = make_clean_recording(2)

    assert not np.array_equal(first.data, second.data)


def test_shape_is_one_channel_at_250_hz_for_300_seconds():
    """One channel named Pz, 250 Hz, 300 seconds of samples."""
    recording = make_clean_recording(1)

    assert recording.ch_names == ["Pz"]
    assert recording.sfreq == 250.0
    assert recording.data.shape == (1, 75000)
    assert recording.is_simulated is True
    assert recording.source == SOURCE_CLEAN


def test_noisy_recording_is_marked_noisy_and_still_valid():
    """The noisy maker uses its own source label and passes validate()."""
    recording = make_noisy_recording(1)

    assert recording.source == SOURCE_NOISY
    assert recording.is_simulated is True
    assert recording.validate() is None


def test_event_labels_are_only_standard_and_target():
    """No other label appears, on either maker."""
    for recording in (make_clean_recording(1), make_noisy_recording(1)):
        labels = {label for _sample, label in recording.events}
        assert labels <= {"standard", "target"}
        assert "target" in labels
        assert "standard" in labels


def test_no_two_targets_are_next_to_each_other():
    """Every target is followed by a standard, on either maker."""
    for recording in (make_clean_recording(1), make_noisy_recording(1)):
        labels = [label for _sample, label in recording.events]
        for left, right in zip(labels, labels[1:]):
            assert not (left == "target" and right == "target")


def test_noisy_recording_has_bigger_bumps_than_clean():
    """The blink bumps make the noisy version visibly larger, in microvolts."""
    clean_peak = float(np.max(np.abs(make_clean_recording(1).data)))
    noisy_peak = float(np.max(np.abs(make_noisy_recording(1).data)))

    # A clean epoch stays well under the 100 uV too-big line.
    assert clean_peak < 100.0
    # The 150 uV blink bumps push the noisy version well past it.
    assert noisy_peak > 100.0
