# LAST STAND — 2D Zombie Survival

A browser-playable 2D zombie survival game built with Streamlit and HTML Canvas/JavaScript. The game runs in the browser; Python/Streamlit provides the app page.

## Features
- Dark, ruined-city background with an atmospheric vignette and debris.
- Zombies spawn around the map and actively chase the player.
- WASD or arrow-key movement.
- Mouse aiming and shooting; Space also fires.
- Health, stamina, ammo, score, waves, and game-over screen.
- Supply crates: move close and press `E` to collect health/ammo.
- Sound effects for firing, hits, collecting supplies, waves, pause, and game over.
- Toggle sound with `M`.
- Pause with `Esc`; restart with `R`.
- No external image or audio assets required; the background and sound effects are generated in the game.

## Run locally (Windows PowerShell)

1. Install Python 3.10 or newer.
2. Open PowerShell in this project folder.
3. Create and activate a virtual environment (optional but recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Check syntax:

   ```powershell
   python -m py_compile app.py
   ```

6. Start the app:

   ```powershell
   streamlit run app.py
   ```

## Controls

| Action | Control |
|---|---|
| Move | `W`, `A`, `S`, `D` or arrow keys |
| Aim | Mouse |
| Shoot | Left mouse click or `Space` |
| Collect nearest supply crate | `E` |
| Pause / resume | `Esc` |
| Restart | `R` |
| Sound on/off | `M` |
| Start / retry | Click or `Enter` |

## Upload to GitHub

1. Create a new repository on GitHub, for example `last-stand-zombie-survival`.
2. Extract this project folder.
3. Upload `app.py`, `requirements.txt`, and `README.md` to the repository.
4. Commit the files.

## Publish a browser-playable version with Streamlit Community Cloud

1. Push the files to GitHub.
2. Open Streamlit Community Cloud: https://share.streamlit.io/
3. Create an app, choose your repository and branch, and set the main file path to `app.py`.
4. Deploy.

## Troubleshooting

- If `python` is not recognized, install Python and enable “Add Python to PATH”.
- If Streamlit is missing, run `python -m pip install -r requirements.txt`.
- If the page does not open automatically, copy the local URL printed by Streamlit into your browser.
- Sound begins after you interact with the game because browsers commonly block audio until a click or key press.
