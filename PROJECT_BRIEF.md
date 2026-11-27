# PROJECT_BRIEF.md - NeuroVault P300 quality-gate app

GOAL
A local, offline Python app. It loads an EEG recording from an auditory oddball test, decides whether the recording is clean enough to trust, and ONLY if so measures P300 latency and amplitude with 95% ranges. It saves results per person and compares a new result with that person's own past results. Its claim: it refuses to answer when the recording is bad, and shows how sure it is when it does answer.

HARD RULES
1. Works with no internet and on battery. No network calls anywhere in the app code.
2. Never use the words diagnosis, risk, normal, abnormal, better or worse in anything the user sees. Results are research measurements, not medical advice.
3. Every simulated or demo recording is labelled SIMULATED or DEMO DATA, on screen and inside saved files.
4. All gate thresholds live in src/config.py and nowhere else. Hardware settings (audio delay, beep settings, headband channel lists) live in src/config_hardware.py, owned by the Engineer.
5. Simple code with plain-English comments. Clear beats clever. No machine learning.
6. Every module has tests in tests/ that run with: pytest
7. All text shown to users lives in src/messages.py.
8. Never put recordings of real people in this repository or in any AI tool.

FILE OWNERSHIP (only the owner edits a file; everyone else asks)
- Lead coder: PROJECT_BRIEF.md, DECISIONS.md, src/recording.py, src/result.py, src/fake_data.py, src/config.py, src/messages.py, src/gate.py, src/simulate.py, src/history.py, src/app.py, src/loaders/openneuro_loader.py, experiments/, and their tests.
- Engineer: src/tone_player.py, src/config_hardware.py, src/loaders/brainflow_loader.py, src/vault.py, tools/calibrate_audio.py, and their tests.
- Support and Testing: docs/, results/ (outputs only), and test logs. Support never edits src/.

CONTRACTS (frozen after Day 3; changes need all three people to agree)
Recording: data (numpy array, channels x samples, in microvolts), sfreq (float), ch_names (list of str), events (list of (sample_index, label), label is "standard", "target" or "distractor"), source (str), subject_id (str), is_simulated (bool, default False).
Result, accepted: status="accepted", channel, latency_ms, latency_range_ms (low, high), amplitude_uv, amplitude_range_uv (low, high), clean_target_count, total_target_count, clean_standard_count, total_standard_count, waveform (times_ms, target_mean, standard_mean, difference), epoch_flags (kept or rejected, and why).
Result, rejected: status="rejected", reason_code, reason_text (plain English), fix_tip, counts.
Reason codes: CHANNEL_MISSING, NO_TARGET_EVENTS, TOO_FEW_TARGETS, TOO_NOISY, NO_CLEAR_P300.
Gate order (built later): choose channel by priority; band-pass filter; cut epochs around standard and target sounds; baseline-correct; flag bad epochs (too big = blinks or movement, too flat = dead sensor); gate the recording (too few clean targets, too few clean epochs); measure on the difference wave (target minus standard) inside the P300 window; bootstrap 95% ranges; reject as NO_CLEAR_P300 if the lower end of the amplitude range is at or below zero or the peak is on the window edge.
