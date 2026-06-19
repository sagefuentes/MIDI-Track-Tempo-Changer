# MIDI Track Tempo Changer

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

A Python data cleaning utility that automatically corrects MIDI file internal tempo metadata by parsing BPM values embedded in filenames. Originally built to fix a specific issue with Ugritone MIDI Drum packs, whose files universally register as 120 BPM internally regardless of their actual tempo — making them uncategorisable by DAWs like Addictive Drums 2 that rely on internal MIDI metadata rather than filenames.

Hopefully useful to others dealing with the same problem.

---

## The Problem

MIDI files store tempo as a `set_tempo` meta-message in the file's internal track data. Many sample packs — including Ugritone's MIDI Drum library — ship with this metadata defaulting to 120 BPM regardless of the actual groove tempo, even when the correct BPM is clearly stated in the filename (e.g. `95bpm_HalfTime_Groove.mid`). DAWs and sample managers that read internal MIDI metadata rather than filenames will therefore miscategorise or misbehave with these files.

This script reads the BPM from the filename and injects or overwrites the `set_tempo` meta-message to match — correcting the metadata without touching any note data.

---

## Features

- **Batch processing** — recursively scans entire directory trees, no manual file-by-file processing
- **Smart BPM detection** — extracts 2–3 digit BPM values from filenames via regex (e.g. `95bpm_`, `120bpm_`, `140BPM_`)
- **Safe metadata correction** — updates existing `set_tempo` messages or inserts one at track 0 if absent; note data is untouched
- **Input validation** — BPM values are constrained to 10–522 BPM matching FL Studio's tempo limits; files outside this range are skipped
- **Error handling** — IOError and ValueError exceptions are caught per file so a single bad file doesn't halt batch processing

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sagefuentes/MIDI-Track-Tempo-Changer.git
   cd MIDI-Track-Tempo-Changer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or with uv:
   ```bash
   uv add mido
   ```

---

## Usage

Run the script and enter the path to your MIDI folder when prompted:

```bash
python "Ugritone Tempo Change.py"
```

The script will recursively scan all subdirectories and process any `.mid` or `.midi` file whose name begins with a valid BPM pattern.

> **Warning:** This script modifies files in place. Back up your MIDI files before running if you want to preserve the originals.

### Supported filename patterns

| Filename | Detected BPM |
|---|---|
| `95bpm_HalfTime.mid` | 95 |
| `120BPM_Groove.midi` | 120 |
| `140bpm_Metal_Fill.mid` | 140 |
| `Groove_120bpm.mid` | ✗ Not detected (BPM must be at start) |

---

## Technical Notes

MIDI tempo is stored as microseconds per beat rather than BPM directly. The `mido` library handles this conversion via `mido.bpm2tempo()`. The script targets the `set_tempo` meta-message type specifically, leaving all other message types (note on/off, control change, etc.) untouched.

---

## Potential Roadmap

- Package as a standalone executable for non-Python users
- Add a `--dry-run` flag to preview changes without writing files
- Generate a log file of processed and failed operations
- Support additional BPM pattern positions in filenames

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
