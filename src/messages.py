"""Every sentence the user can see, in one place (PROJECT_BRIEF.md hard rule 7).

Code should import these names and never type user-facing text inline.
Keep this file free of the banned words: diagnosis, risk, normal, abnormal,
better, worse. The one exception is FIXED_NOTE, which is a fixed legal-style
line agreed in the brief. tests/test_messages.py enforces this.
"""

# Banners that say where a recording came from. They must never be mixed up.
BANNER_SAVED = "SAVED RECORDING - not a live brain"
BANNER_SIMULATED = "SIMULATED - damaged copy of a real recording"
BANNER_LIVE = "LIVE HEADBAND"

# Label for demo material, shown on screen and written inside saved files.
LABEL_DEMO = "DEMO DATA"

# Heading for the screen shown after the gate refuses a recording.
TITLE_TRY_AGAIN = "Try again"

# Fixed note that goes with every result. Wording is agreed and must not change.
FIXED_NOTE = "This tool is not a diagnosis. If you are worried about memory changes, talk to a doctor."

# Plain-English reason shown when the gate rejects a recording.
REASON_TEXT_CHANNEL_MISSING = "The headband did not send the channel we need (Pz or Cz)."
REASON_TEXT_NO_TARGET_EVENTS = "No target sounds were marked in this recording, so there is nothing to measure."
REASON_TEXT_TOO_FEW_TARGETS = "There were not enough target sounds to measure safely."
REASON_TEXT_TOO_NOISY = "Too many parts of this recording were too big (blinks or movement) or too flat (a loose sensor)."
REASON_TEXT_NO_CLEAR_P300 = "The recording was clean, but no clear P300 bump stood out from chance."

# One practical hint shown under each reason.
FIX_TIP_CHANNEL_MISSING = "Check that the headband is switched on and connected, then run the test again."
FIX_TIP_NO_TARGET_EVENTS = "Check that the sound markers were saved with the recording, then run the test again."
FIX_TIP_TOO_FEW_TARGETS = "Run the full test from start to finish without stopping it early."
FIX_TIP_TOO_NOISY = "Ask the person to sit still with the sensor pressed on the scalp, then run the test again."
FIX_TIP_NO_CLEAR_P300 = "Run the test again; if this repeats, show the recording to your team lead."
