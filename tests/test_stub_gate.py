"""Tests for the temporary stub in src/gate.py: the answer shape, not the maths.

The stub only exists so later screens can be built. These tests check that it
returns the right kind of result for each fake source; Stage 4 replaces both
the stub and the parts of these tests that describe placeholder values.
"""

from src.fake_data import SOURCE_CLEAN, SOURCE_NOISY, make_clean_recording, make_noisy_recording
from src.gate import check_recording
from src.messages import FIX_TIP_TOO_NOISY, REASON_TEXT_TOO_NOISY
from src.result import TOO_NOISY, AcceptedResult, RejectedResult


def test_clean_fake_source_is_accepted():
    """A FAKE-CLEAN recording comes back as an accepted result."""
    result = check_recording(make_clean_recording(1))

    assert isinstance(result, AcceptedResult)
    assert result.status == "accepted"
    assert result.channel == "Pz"


def test_accepted_result_has_the_full_shape():
    """The accepted placeholder carries every field a screen will read."""
    result = check_recording(make_clean_recording(1))

    assert set(result.waveform) == {
        "times_ms",
        "target_mean",
        "standard_mean",
        "difference",
    }
    assert len(result.latency_range_ms) == 2
    assert len(result.amplitude_range_uv) == 2
    assert result.total_target_count > 0
    assert result.clean_target_count == result.total_target_count


def test_noisy_fake_source_is_rejected_as_too_noisy():
    """A FAKE-NOISY recording comes back rejected, with the TOO_NOISY code."""
    result = check_recording(make_noisy_recording(1))

    assert isinstance(result, RejectedResult)
    assert result.status == "rejected"
    assert result.reason_code == TOO_NOISY


def test_rejected_result_carries_its_plain_english_text():
    """The rejected placeholder uses the agreed message text and hint."""
    result = check_recording(make_noisy_recording(1))

    assert result.reason_text == REASON_TEXT_TOO_NOISY
    assert result.fix_tip == FIX_TIP_TOO_NOISY
    assert result.counts["total_target_count"] > 0


def test_the_two_fake_sources_get_different_sources():
    """Guards the two source labels the stub branches on."""
    assert make_clean_recording(1).source == SOURCE_CLEAN
    assert make_noisy_recording(1).source == SOURCE_NOISY
