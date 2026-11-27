"""The Recording object: one EEG recording plus what we know about it.

This is the frozen contract from PROJECT_BRIEF.md. Every loader must produce
one of these, and every later stage (gate, measure, history) accepts one.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

# The only event labels the oddball test uses.
ALLOWED_LABELS = ("standard", "target", "distractor")


@dataclass
class Recording:
    """One EEG recording, ready to be checked.

    data:      numpy array, channels x samples, in microvolts.
    sfreq:     sampling rate in Hz (samples per second).
    ch_names:  channel name for each row of data, e.g. ["Pz", "Cz"].
    events:    list of (sample_index, label) pairs marking each sound.
    source:    where the recording came from, e.g. "brainflow" or "simulated".
    subject_id: who the recording belongs to (a code, never a real name).
    is_simulated: True if this is SIMULATED or DEMO DATA, so it can be labelled.
    """

    data: np.ndarray
    sfreq: float
    ch_names: List[str]
    events: List[Tuple[int, str]]
    source: str
    subject_id: str
    is_simulated: bool = False

    def validate(self) -> None:
        """Raise ValueError with a plain-English message if the recording is malformed.

        Returns None when the recording is well formed.
        """
        # Work on an array view so plain nested lists also give clear errors.
        data = np.asarray(self.data)

        # A recording must be a 2-D grid: channels (rows) x samples (columns).
        if data.ndim != 2:
            raise ValueError(
                "Recording data must be 2-dimensional (channels x samples), "
                f"but it has {data.ndim} dimension(s)."
            )

        # Each row needs exactly one channel name.
        n_channels, n_samples = data.shape
        if n_channels != len(self.ch_names):
            raise ValueError(
                f"Recording data has {n_channels} row(s) but ch_names has "
                f"{len(self.ch_names)} name(s); they must match one-to-one."
            )

        # Every event must point at a real sample inside the recording,
        # and must be a label this test understands.
        for sample_index, label in self.events:
            if sample_index < 0:
                raise ValueError(
                    f"Event sample index {sample_index} is negative; "
                    "events must point at sample 0 or later."
                )
            if sample_index >= n_samples:
                raise ValueError(
                    f"Event sample index {sample_index} is past the last sample "
                    f"({n_samples - 1}); the recording only has {n_samples} samples."
                )
            if label not in ALLOWED_LABELS:
                raise ValueError(
                    f"Event label {label!r} is not allowed; use one of "
                    f"{', '.join(ALLOWED_LABELS)}."
                )
