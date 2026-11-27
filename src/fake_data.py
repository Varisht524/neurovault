"""Fake recordings for demos and tests, so nothing real is ever needed.

Two makers live here. Both build the same oddball test: one channel called Pz,
250 samples per second, 300 seconds long, a quiet background, and a beep every
1.3 seconds. One in five beeps is a target; the rest are standards. A target
gets a small smooth bump about 380 ms after the beep, which stands in for a
P300. The noisy maker also drops large blink bumps into some epochs.

Everything is built from a seed, so the same seed always gives the same
recording. These recordings are always marked is_simulated = True.
"""

import numpy as np

from src.recording import Recording

# Fixed shape of every fake recording.
SAMPLE_RATE_HZ = 250.0
DURATION_S = 300.0
CHANNEL_NAME = "Pz"

# One beep every 1.3 seconds.
BEEP_INTERVAL_S = 1.3
# One beep in five is a target.
TARGET_FRACTION = 0.2

# Background noise size, in microvolts (about 10 uV of wobble).
BACKGROUND_UV = 10.0

# The P300 stand-in: a smooth bump that peaks this long after the beep.
P300_PEAK_S = 0.38
P300_SIZE_UV = 6.0
P300_WIDTH_S = 0.08

# The blink stand-in: a much bigger bump on a share of epochs.
BLINK_FRACTION = 0.4
BLINK_SIZE_UV = 150.0
BLINK_PEAK_S = 0.3
BLINK_WIDTH_S = 0.12

# Where the recording came from, written into the Recording.source field.
SOURCE_CLEAN = "FAKE-CLEAN"
SOURCE_NOISY = "FAKE-NOISY"

# A code used instead of a real person's name.
FAKE_SUBJECT_ID = "FAKE-001"


def _add_bump(row, center_sample, size_uv, width_s, sample_rate):
    """Add one smooth bell-shaped bump to a channel, in place.

    row:          the channel data to change (1-D array).
    center_sample: sample where the bump is tallest.
    size_uv:      how tall the bump is, in microvolts.
    width_s:      how wide the bump is, in seconds.
    """
    width_samples = width_s * sample_rate
    # A bell curve centred on center_sample.
    times = np.arange(len(row), dtype=float)
    row += size_uv * np.exp(-0.5 * ((times - center_sample) / width_samples) ** 2)


def _make_recording(seed, source, add_blinks):
    """Build one fake recording. This is the shared body of both makers.

    seed:       number that fixes the random parts, so runs repeat exactly.
    source:     the source label, FAKE-CLEAN or FAKE-NOISY.
    add_blinks: True to drop large blink bumps into about 40% of epochs.
    """
    rng = np.random.default_rng(seed)

    sample_rate = SAMPLE_RATE_HZ
    n_samples = int(round(DURATION_S * sample_rate))
    beep_step = int(round(BEEP_INTERVAL_S * sample_rate))

    # Start with quiet background noise on the single channel.
    data = rng.standard_normal((1, n_samples)) * BACKGROUND_UV
    row = data[0]

    # Work out the beep times and their labels.
    # Keep only beeps whose whole epoch fits inside the recording.
    last_start = int(P300_PEAK_S * sample_rate) + beep_step
    events = []
    seen_target = False
    for start in range(beep_step, n_samples - last_start, beep_step):
        # A target is allowed only after a standard, so two never touch.
        if not seen_target and rng.random() < TARGET_FRACTION:
            label = "target"
        else:
            label = "standard"
        events.append((start, label))
        seen_target = label == "target"

    for start, label in events:
        if label == "target":
            # The smooth P300 stand-in, peaking about 380 ms after the beep.
            _add_bump(
                row,
                start + P300_PEAK_S * sample_rate,
                P300_SIZE_UV,
                P300_WIDTH_S,
                sample_rate,
            )

        if add_blinks and rng.random() < BLINK_FRACTION:
            # A large blink bump, tall enough that the epoch looks too big.
            _add_bump(
                row,
                start + BLINK_PEAK_S * sample_rate,
                BLINK_SIZE_UV,
                BLINK_WIDTH_S,
                sample_rate,
            )

    recording = Recording(
        data=data,
        sfreq=sample_rate,
        ch_names=[CHANNEL_NAME],
        events=events,
        source=source,
        subject_id=FAKE_SUBJECT_ID,
        is_simulated=True,
    )

    # Catch a broken fake early, before any demo or test uses it.
    recording.validate()
    return recording


def make_clean_recording(seed):
    """A fake recording with a clear P300 stand-in and no blink bumps."""
    return _make_recording(seed, SOURCE_CLEAN, add_blinks=False)


def make_noisy_recording(seed):
    """A fake recording with large blink bumps on about 40% of the epochs."""
    return _make_recording(seed, SOURCE_NOISY, add_blinks=True)
