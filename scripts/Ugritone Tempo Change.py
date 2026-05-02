"""
A script to update MIDI file tempos based on their filenames, consistent with the style for Ugritone MIDI Drum tracks.


This module scans a directory for MIDI files with filename starting with 'xxbpm' or 'xxxbpm',
extracts the BPM value, and updates the internal MIDI tempo meta-message.
"""

import os
import re
from typing import Optional
import mido


def get_bpm_from_filename(filename: str) -> Optional[int]:
    """Extracts the BPM from the start of a filename.

    Args:
        filename: The name of the file to check.

    Returns:
        The extracted BPM as an integer, or None if the pattern doesn't match.
    """
    # Matches 2-3 digits followed by 'bpm' at the start of the string.
    match = re.match(r'^(\d{2,3})bpm', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def update_midi_tempo(file_path: str, bpm: int) -> None:
    """Updates or inserts a set_tempo meta-message in a MIDI file.

    Args:
        file_path: Path to the MIDI file.
        bpm: The beats per minute to set.
    """
    new_tempo = mido.bpm2tempo(bpm)
    try:
        mid = mido.MidiFile(file_path)
        tempo_updated = False

        for track in mid.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    msg.tempo = new_tempo
                    tempo_updated = True

        if not tempo_updated:
            # If no tempo message exists, insert it at the start of track 0.
            mid.tracks[0].insert(0, mido.MetaMessage('set_tempo', tempo=new_tempo))

        mid.save(file_path)
        print(f"Updated '{os.path.basename(file_path)}' to {bpm} BPM.")
    except (IOError, ValueError) as e:
        print(f"Failed to process '{file_path}': {e}")


def process_directory(root_directory: str) -> None:
    """Recursively iterates through folders to process MIDI files.

        Args:
            root_directory: The top-level folder to start the search from.
        """
    if not os.path.isdir(root_directory):
        print(f"Error: The directory '{root_directory}' does not exist.")
        return

    # os.walk yields a 3-tuple: (dirpath, dirnames, filenames)
    for root, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith(('.mid', '.midi')):
                bpm = get_bpm_from_filename(filename)
                if bpm and 10<= bpm <= 522: #constraints for bpm based on FL Studio tempo limits
                    full_path = os.path.join(root, filename)
                    update_midi_tempo(full_path, bpm)


if __name__ == '__main__':
    folder = input("Enter the path to the folder with MIDI files: ").strip()
    if os.path.isdir(folder):
        process_directory(folder)
        print("Conversion complete.")
    else:
        print("Invalid folder path.")