# All values are starting guesses to be tuned on real data. Never loosen them to make a headband pass. Every change must be logged in DECISIONS.md.

# Band-pass filter: keep signals between these two frequencies, in Hz.
FILTER_LOW_HZ = 0.5
FILTER_HIGH_HZ = 20.0

# Cut each epoch this far before the sound, in seconds.
EPOCH_TMIN_S = -0.2
# Cut each epoch this far after the sound, in seconds.
EPOCH_TMAX_S = 0.8

# Baseline starts here, in seconds, so we can subtract the pre-sound level.
BASELINE_TMIN_S = -0.2
# Baseline ends at the moment of the sound, in seconds.
BASELINE_TMAX_S = 0.0

# An epoch is too big (likely blink or movement) above this peak-to-peak size, in microvolts.
MAX_PEAK_TO_PEAK_UV = 100.0
# An epoch is too flat (likely dead sensor) below this peak-to-peak size, in microvolts.
MIN_PEAK_TO_PEAK_UV = 0.5

# Need at least this many clean target epochs before we answer at all.
MIN_CLEAN_TARGETS = 15
# Need at least this fraction of the target epochs to be clean before we answer at all.
MIN_CLEAN_FRACTION = 0.5

# Look for the P300 peak only between these times after the sound, in milliseconds.
P300_WINDOW_MS = (250, 600)

# Resample the data this many times to get the 95% range.
N_BOOTSTRAP = 1000
# The range covers this percent of resampled values.
RANGE_PERCENT = 95
# Fixed seed so the same recording gives the same answer every run.
RANDOM_SEED = 0

# Try these channels in this order and use the first one that is present.
CHANNEL_PRIORITY = ["Pz", "Cz"]
