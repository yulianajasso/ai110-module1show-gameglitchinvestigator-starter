# Bugs

## Bug #1 — Reversed hints

**Symptom:** Student says "the hints are wrong" but can't pinpoint the code.

**Redirect:** "Find the `check_guess` function in `app.py`. Read lines 37–40 aloud. What does it return when `guess > secret`? What should it return?"

## Bug #2 — String conversion on even attempts (the "random" bug)

**Symptom:** Student describes the game as "sometimes broken" or "random." This is the hardest bug to find without guidance.

**Redirect:** "Open the Developer Debug Info expander at the bottom of the app. Make a guess and watch the attempts counter. Try guessing the exact secret number on attempt 1, then again on attempt 2. Is the behavior different?" After they notice: "Find lines 158–161 in `app.py`. What does that `if attempts % 2 == 0` branch do to the secret?"

## Bug #3 — New Game doesn't reset state

**Symptom:** Student finishes a game (wins or loses), clicks **New Game 🔁**, but the app still shows "You already won..." or "Game over..." and won't let them play again.

**Redirect:** "Find the `new_game` button handler (the `if new_game:` block around lines 134–138 in `app.py`). List every session state key it resets. Now look at line 140 — what condition has to be true for the game to let you play? Which key does the game use to track win/lose status, and is it in the list of things New Game resets? What value does it need to be?" (`st.session_state.status` is not reset.)

## Bug #4 — Prompt shows the wrong range

**Symptom:** Student picks Easy or Hard, but the instructions still say "Guess a number between 1 and 100," which doesn't match the sidebar range.

**Redirect:** "Look at the `st.info(...)` message around lines 109–112 in `app.py`. Is the range hardcoded or computed? Where do `low` and `high` get set, and are they used here?"

## Bug #5 — New Game ignores the difficulty range

**Symptom:** On Easy (1–20), after clicking New Game the secret seems impossible to guess — it's outside the range shown.

**Redirect:** "Find the `if new_game:` block around line 136. What numbers are passed to `random.randint`? Compare that to how the secret is first created at line 93. What's different?"

## Bug #6 — Attempts counter starts inconsistently

**Symptom:** "Attempts left" looks off by one on the very first game compared to after clicking New Game.

**Redirect:** "Find where `attempts` is first set in session state around line 95–96. What value does it start at? Now look at what New Game resets it to around line 135. Should those two match?"

## Bug #7 — Scoring rewards wrong guesses

**Symptom:** Student notices their score sometimes goes *up* after a guess that was too high.

**Redirect:** "Find the `update_score` function around lines 50–65 in `app.py`. Read the `Too High` branch. Under what condition does it add points instead of subtracting? Should guessing too high ever increase your score? Compare it to the `Too Low` branch."

## Bug #8 — Difficulty levels are backwards

**Symptom:** "Hard" feels easier than "Normal" — the range of numbers is smaller.

**Redirect:** "Find `get_range_for_difficulty` around lines 4–11 in `app.py`. Compare the ranges for Normal and Hard. Which one covers more numbers? Which difficulty *should* cover more numbers?"

## Bug #9 — Win score is off by one

**Symptom:** Winning on the first guess gives fewer points than expected (80 instead of 90).

**Redirect:** "Find the `Win` branch of `update_score` around line 52. Walk through the points formula with `attempt_number = 1`. What does the `+ 1` do to the result? Is that intended?"

## Bug #10 — Decimal guesses are silently truncated

**Symptom:** Student types `3.9`, the game treats it as `3` with no warning.

**Redirect:** "Find `parse_guess` around lines 14–29 in `app.py`. What happens when the input contains a `.`? Does `int(float(raw))` round or truncate? Should a decimal guess be accepted, rejected, or rounded?"

