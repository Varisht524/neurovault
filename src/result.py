"""The two result objects from PROJECT_BRIEF.md.

AcceptedResult is only produced when the recording passed the gate.
RejectedResult is produced when it did not, and says why in plain English.
Both are plain dataclasses with no logic, so they are easy to save and compare.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

# The five reason codes a rejected result can carry (frozen contract).
CHANNEL_MISSING = "CHANNEL_MISSING"
NO_TARGET_EVENTS = "NO_TARGET_EVENTS"
TOO_FEW_TARGETS = "TOO_FEW_TARGETS"
TOO_NOISY = "TOO_NOISY"
NO_CLEAR_P300 = "NO_CLEAR_P300"


@dataclass
class AcceptedResult:
    """A measurement we trust, produced only for a recording that passed the gate.

    latency_ms:           peak time after the sound, in milliseconds.
    latency_range_ms:     (low, high) 95% range around latency_ms.
    amplitude_uv:         peak size of the difference wave, in microvolts.
    amplitude_range_uv:   (low, high) 95% range around amplitude_uv.
    waveform:             dict with times_ms, target_mean, standard_mean, difference.
    epoch_flags:          one dict per epoch saying kept or rejected, and why.
    """

    # Fixed status word so anyone reading a saved file can tell what it is.
    status: str = field(default="accepted", init=False)
    channel: str = ""
    latency_ms: float = 0.0
    latency_range_ms: tuple = (0.0, 0.0)
    amplitude_uv: float = 0.0
    amplitude_range_uv: tuple = (0.0, 0.0)
    clean_target_count: int = 0
    total_target_count: int = 0
    clean_standard_count: int = 0
    total_standard_count: int = 0
    waveform: Dict[str, Any] = field(default_factory=dict)
    epoch_flags: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class RejectedResult:
    """The gate refused to answer, and this says why and what to try next.

    reason_text is plain English for the screen; fix_tip is one practical hint.
    counts holds the numbers the gate looked at, e.g. clean and total targets.
    """

    # Fixed status word so anyone reading a saved file can tell what it is.
    status: str = field(default="rejected", init=False)
    reason_code: str = ""
    reason_text: str = ""
    fix_tip: str = ""
    counts: Dict[str, int] = field(default_factory=dict)
