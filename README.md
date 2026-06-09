# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** A Streamlit number-guessing game: the app picks a secret number in a range based on difficulty, and the player guesses, getting "Too High" / "Too Low" hints and a running score until they win or run out of attempts.
- [x] **Detail which bugs you found.**
  - **Bug #1 — Reversed hints.** A guess that was too high told the player to "Go HIGHER" (and vice versa), so the hints pointed the wrong way.
  - **Bug #2 — "Random" win bug.** On even-numbered attempts the secret was cast to a string, so a correct numeric guess (`42 == "42"`) was `False` and never registered as a win.
  - **Bug #3 — New Game stuck.** After a win/loss, "New Game" only reset `attempts` and `secret`, leaving `status` on "won"/"lost", so the game refused to start a new round.
- [x] **Explain what fixes you applied.**
  - Refactored the pure logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` into `logic_utils.py` so it could be unit-tested without Streamlit.
  - Bug #1: swapped the hint messages back so too-high says "Go LOWER" and too-low says "Go HIGHER".
  - Bug #2: removed the even-attempt string cast so the secret always stays an `int`.
  - Bug #3: the New Game handler now resets `status`, `history`, and `score` in addition to `attempts` and `secret`.

## 📸 Demo Walkthrough

A sample game on Normal difficulty (range 1–100), where the secret is **57**:

1. User enters a guess of **40** → game returns **"📈 Go HIGHER!"** (Too Low).
2. User enters a guess of **70** → game returns **"📉 Go LOWER!"** (Too High).
3. User enters a guess of **57** → game returns **"🎉 Correct!"** and shows balloons.
4. Score updates after each guess, and the final winning score is displayed.
5. User clicks **New Game 🔁** → the board resets (status, history, score, attempts, and a fresh secret) and a brand-new round begins.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.13.1, pytest-9.0.3, pluggy-1.6.0
collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 16%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 50%]
tests/test_game_logic.py::test_too_high_hint_tells_player_to_go_lower PASSED [ 66%]
tests/test_game_logic.py::test_too_low_hint_tells_player_to_go_higher PASSED [ 83%]
tests/test_game_logic.py::test_correct_int_guess_always_wins PASSED      [100%]

============================== 6 passed in 0.01s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
