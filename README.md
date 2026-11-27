# NeuroVault

NeuroVault is a local, offline Python app built as a school competition prototype. It loads an EEG recording from an auditory oddball test and decides whether that recording is clean enough to trust, and only then measures P300 latency and amplitude with 95% ranges. It saves results per person, compares a new result with that person's own past results, and refuses to answer when the recording is bad.

## Setup

Run these from the project root. They only need to be done once.

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it (macOS / Linux)
source venv/bin/activate

#    On Windows instead:
#    venv\Scripts\activate

# 3. Install the pinned packages
pip install -r requirements.txt
```

The finished app must run with no internet connection, but installing the packages above needs a connection once.

## Running the tests

```bash
pytest
```

Every module has tests in `tests/`. The suite also includes a guard test (`tests/test_no_network.py`) that fails if any file under `src/` contains network code, and a message test (`tests/test_messages.py`) that fails if user-facing text contains banned words.

## Folder layout

```
NeuroVault/
├── PROJECT_BRIEF.md        # the rules, contracts and file ownership for the team
├── README.md               # this file
├── DECISIONS.md            # log of every threshold change
├── requirements.txt        # the ten pinned packages
├── .gitignore
├── .streamlit/
│   └── config.toml         # Streamlit settings (usage stats off)
├── src/                    # all app code
│   ├── config.py           # every gate threshold lives here and nowhere else
│   ├── messages.py         # every sentence the user can see
│   ├── recording.py        # the Recording object and its validate() checks
│   ├── result.py           # AcceptedResult, RejectedResult, reason codes
│   ├── gate.py             # the quality gate (stub for now)
│   └── loaders/            # recording loaders
├── tests/                  # tests for every module, run with pytest
├── data/                   # raw recordings (not in git)
├── sessions/               # per-person saved results (not in git)
├── results/                # outputs only
├── experiments/            # experiment scripts and notes
├── tools/                  # helper scripts, e.g. audio calibration
└── docs/                   # support and testing documentation
```

`data/` and `sessions/` are listed in `.gitignore`, so they stay on the machine and never go into the repository.

## File ownership

Only the owner edits a file; everyone else asks.

- **Lead coder:** `PROJECT_BRIEF.md`, `DECISIONS.md`, `src/recording.py`, `src/result.py`, `src/fake_data.py`, `src/config.py`, `src/messages.py`, `src/gate.py`, `src/simulate.py`, `src/history.py`, `src/app.py`, `src/loaders/openneuro_loader.py`, `experiments/`, and their tests.
- **Engineer:** `src/tone_player.py`, `src/config_hardware.py`, `src/loaders/brainflow_loader.py`, `src/vault.py`, `tools/calibrate_audio.py`, and their tests.
- **Support and Testing:** `docs/`, `results/` (outputs only), and test logs. Support never edits `src/`.
