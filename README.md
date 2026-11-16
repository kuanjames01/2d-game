# 2d-game

## Run on Windows

The sound effects use Pygame's mixer and require an available audio output device.
For reliable playback, open this folder in a local Windows VS Code window (not a
WSL Remote window), select a Windows Python interpreter, and install the
dependency. If you have Anaconda installed in your user folder, create and use
a project environment from PowerShell with:

```powershell
& "$env:USERPROFILE\anaconda3\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

In VS Code, choose **Python: Select Interpreter** and select that same Windows
`.venv` interpreter. If Windows Python is installed elsewhere, replace the
Anaconda path with its path. Running with WSL Python requires a working WSL
audio device; a missing device cannot produce sound.