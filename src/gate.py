"""The quality gate: the single place that decides if a recording can be trusted.

TEMPORARY STUB. Builds the result shape only, with fixed placeholder numbers.
The real gate is built in Stage 4 and will follow the gate order written in
PROJECT_BRIEF.md, using thresholds from src/config.py.
"""

import numpy as np

from src.messages import (
    FIX_TIP_TOO_NOISY,
    REASON_TEXT_TOO_NOISY,
)
from src.recording import Recording
from src.result import TOO_NOISY, AcceptedResult, RejectedResult


def check_recording(recording: Recording):
    """Return an answer for this recording.

    ============================== THIS IS A STUB ==============================
    It does not measure anything. A recording from the clean fake maker gets an
    accepted result with made-up placeholder numbers, and every other recording
    is rejected as TOO_NOISY. Stage 4 replaces this whole function with the real
    gate: choose channel, filter, cut epochs, flag bad epochs, count clean
    targets, measure, and bootstrap the 95% ranges.
    ===========================================================================
    """
    total_targets = sum(1 for _sample, label in recording.events if label == "target")
    total_standards = sum(1 for _sample, label in recording.events if label == "standard")

    if recording.source == "FAKE-CLEAN":
        return AcceptedResult(
            channel=recording.ch_names[0],
            latency_ms=350.0,
            latency_range_ms=(320.0, 380.0),
            amplitude_uv=4.0,
            amplitude_range_uv=(3.0, 5.0),
            clean_target_count=total_targets,
            total_target_count=total_targets,
            clean_standard_count=total_standards,
            total_standard_count=total_standards,
            waveform={
                "times_ms": np.array([0.0]),
                "target_mean": np.array([0.0]),
                "standard_mean": np.array([0.0]),
                "difference": np.array([0.0]),
            },
            epoch_flags=[],
        )

    return RejectedResult(
        reason_code=TOO_NOISY,
        reason_text=REASON_TEXT_TOO_NOISY,
        fix_tip=FIX_TIP_TOO_NOISY,
        counts={
            "total_target_count": total_targets,
            "total_standard_count": total_standards,
        },
    )
