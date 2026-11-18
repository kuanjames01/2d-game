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

## Gameplay progression

Move with the arrow keys or **WASD** and keep shooting; the player fires
automatically. Meteor waves become faster and more frequent as the run
progresses. Boss encounters begin after 30 seconds and recur after each boss
defeat, up to Level 15. Each encounter uses three randomly selected abilities.
Defeating the Level 15 boss starts Endless Survival, where meteors continue
spawning and the HUD tracks survival time until the player's health reaches
zero.