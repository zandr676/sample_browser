# sample_browser

Sample Browser - Audio Sample Library Manager
============================================

OVERVIEW
--------
Sample Browser is a Python application that helps you browse, search, filter, and preview audio samples from your sample library. It automatically extracts BPM and key information from filenames and allows you to drag samples directly into your DAW.

FEATURES
--------
- Browse audio samples (.wav, .aif, .aiff, .mp3, .flac)
- Search samples by filename
- Filter by BPM range and musical key
- Single-click audio preview/playback
- Drag and drop samples into your DAW
- Automatic BPM and key detection from filenames
- Automatically finds Splice directory on first run

REQUIREMENTS
------------
- Python 3.6 or higher
- PyQt5
- pygame

INSTALLATION
------------
1. Install Python from https://www.python.org/downloads/

2. Install required packages:
   pip install PyQt5 pygame

3. Download sample_browser.py to your desired location

USAGE
-----
1. Run the application:
   python sample_browser.py

2. On first run:
   - If you have Splice installed, it will automatically use your Splice sounds directory
   - Otherwise, select your sample library folder when prompted

3. Browse and search:
   - Type in the search box to filter by filename
   - Set BPM range using the min/max fields
   - Select a key from the dropdown to filter by musical key

4. Preview samples:
   - Single-click any sample to play it
   - Click the same sample again to stop playback
   - Click a different sample to switch playback

5. Use samples in your DAW:
   - Select one or more samples (Ctrl/Cmd+click for multiple)
   - Drag and drop into your DAW project

FILENAME CONVENTIONS
-------------------
The application extracts metadata from filenames using these patterns:

BPM Detection:
- "120bpm" or "120_bpm" or "120-bpm"
- "bpm120" or "bpm_120" or "bpm-120"
- "_120_" (number between underscores)

Key Detection:
- "C", "C#", "Cm", "Cmin", "Cmaj", "Cmajor"
- Supports all musical keys (A-G) with sharps/flats
- Recognizes major/minor variations

Example filenames:
- "Drum_Loop_120bpm_Cmaj.wav"
- "Bass_Hit_F#m_140_BPM.wav"
- "Synth_Lead_90bpm.mp3"

TROUBLESHOOTING
--------------
1. No audio playback:
   - Ensure pygame is properly installed
   - Check that your audio device is working
   - Unsupported formats will show error in console

2. Samples not found:
   - Make sure you selected the correct directory
   - Check that your samples use supported formats
   - Verify file permissions

3. BPM/Key not detected:
   - Check that filenames follow conventions above
   - BPM must be between 60-200 to be detected
   - Key detection requires standard notation

KEYBOARD SHORTCUTS
-----------------
- Ctrl/Cmd + Click: Select multiple samples
- Shift + Click: Select range of samples

NOTES
-----
- The application remembers the currently playing sample
- Filtering or updating the table stops playback
- Enharmonic equivalents are handled (C# = Db, etc.)
- Sample paths are preserved for drag and drop

VERSION
-------
1.0.0

AUTHOR
------
Claude Opus 4 w HITL

LICENSE
-------
CC0 1.0

CC0 1.0 Universal
By marking the work with a CC0 public domain dedication, the creator is giving up their copyright and allowing reusers to distribute, remix, adapt, and build upon the material in any medium or format, even for commercial purposes.

CC0 This work has been marked as dedicated to the public domain.
