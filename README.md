# MIDI Tempo Auto-Updater

A Python data cleaning utility to automatically update MIDI file internal tempo metadata based on filenames. 
Specifically designed to match the naming convention used by Ugritone MIDI Drum tracks since their old files all register as 120bpm.
Designed this as the metadata for MIDI is a little trickier to access directly and Addictive Drums 2 uses internal MIDI data to categorize general MIDI files.
Hopefully, it can help someone else too!

## Features
* **Batch Processing:** Scans entire directories and subdirectories.
* **Smart Detection:** Extracts BPM from filenames starting with 2 or 3 digits (e.g., `120bpm_Groove.mid`).
* **Metadata Correction:** Injects or updates the `set_tempo` meta-message without altering note data.

## Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Usage   
After installation, run the script, it will ask you for the path to the folder you wish to process.
It will scan the entire directory/folder and all subdirectories/subfolders.

### *Warning:* 
Due to the process changing metadata, I do recommend backing up MIDI tracks before just in case you wish to revert for some reason.

## Support
Feel free to open an issue here if there is anything I can help with!

## Potential Roadmap
* Turn script into simple executable.
* Give additional options for various renaming. 
* Generate text file of failed operations.

## License

[MIT](https://choosealicense.com/licenses/mit/)