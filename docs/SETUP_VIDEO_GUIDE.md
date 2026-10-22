# Task 1: Environment Setup Video Demonstration Guide

## Instructions for Recording (1–2 minutes)

The assignment rubric requires a short recorded video demonstrating the project environment setup.

### How to record (Windows):
1. Press `Win + Alt + R` (Windows built-in screen recorder) or use OBS Studio / Clipchamp.
2. Open terminal in the project directory: `SQE_Assignment`.

### Script / Commands to show in the video:
1. Show your Python version:
   ```bash
   python --version
   ```
2. Demonstrate creating and activating the virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Demonstrate installing all project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Verify tests run successfully:
   ```bash
   pytest
   ```
5. Save the recorded video as `docs/setup_video.mp4` and commit it to the repository (or upload to Google Drive/YouTube and link it in the `README.md` if the video is over GitHub's file limit).
