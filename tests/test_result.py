"""Tests for src/result.py: both result objects exist and the reason codes are set."""

from src.result import (
    CHANNEL_MISSING,
    NO_CLEAR_P300,
    NO_TARGET_EVENTS,
    TOO_FEW_TARGETS,
    TOO_NOISY,
    AcceptedResult,
    RejectedResult,
)


def test_accepted_result_can_be_created():
    """An accepted result holds the brief's fields and is marked accepted."""
    result = AcceptedResult(
        channel="Pz",
        latency_ms=320.0,
        latency_range_ms=(300.0, 340.0),
        amplitude_uv=4.2,
        amplitude_range_uv=(3.1, 5.3),
        clean_target_count=28,
        total_target_count=30,
        clean_standard_count=90,
        total_standard_count=100,
        waveform={
            "times_ms": [-200, 0, 200],
            "target_mean": [0.0, 1.0, 2.0],
            "standard_mean": [0.0, 0.5, 1.0],
            "difference": [0.0, 0.5, 1.0],
        },
        epoch_flags=[{"kept": True, "reason": ""}],
    )
    assert result.status == "accepted"
    assert result.channel == "Pz"
    assert result.latency_range_ms == (300.0, 340.0)
    assert result.total_target_count == 30


def test_rejected_result_can_be_created():
    """A rejected result holds a reason and counts and is marked rejected."""
    result = RejectedResult(
        reason_code=TOO_NOISY,
        reason_text="The recording was too noisy to measure.",
        fix_tip="Ask the person to sit still and run the test again.",
        counts={"clean_targets": 6, "total_targets": 30},
    )
    assert result.status == "rejected"
    assert result.reason_code == "TOO_NOISY"
    assert result.counts["total_targets"] == 30


def test_reason_codes_exist():
    """All five frozen reason codes are module-level string constants."""
    assert CHANNEL_MISSING == "CHANNEL_MISSING"
    assert NO_TARGET_EVENTS == "NO_TARGET_EVENTS"
    assert TOO_FEW_TARGETS == "TOO_FEW_TARGETS"
    assert TOO_NOISY == "TOO_NOISY"
    assert NO_CLEAR_P300 == "NO_CLEAR_P300"
