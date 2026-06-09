# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran the game it launched fine and looked normal, but the gameplay was clearly broken. I found three concrete bugs:

- **Bug #1 — Reversed hints.** *Expected:* when my guess is higher than the secret, the hint should tell me to go LOWER. *Actual:* the hint told me to go HIGHER, so the directions were backwards and following them led me away from the answer.
- **Bug #2 — "Random" string-comparison bug on even attempts.** *Expected:* guessing the exact secret number should always win, no matter which attempt I'm on. *Actual:* the game felt randomly broken — on even-numbered attempts the secret gets converted to a string, so a correct numeric guess is compared against text and never registers as a win, giving wrong hints instead.
- **Bug #3 — New Game doesn't reset state.** *Expected:* after winning or losing, clicking "New Game" should let me play again. *Actual:* it still showed "You already won..." / "Game over..." and refused to start because the win/lose `status` was never reset.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 60 when secret is 40 | "Too High" hint → go LOWER | "Go HIGHER!" hint shown (directions reversed) | none |
| Guess the exact secret on attempt 2 (an even attempt) | "🎉 Correct!" — win | Treated as wrong; a Too High/Too Low hint shown instead of a win | none |
| Win or lose, then click "New Game" | Game resets and lets me play again | Still shows "You already won." / "Game over." and won't start | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used my AI coding assistant inside VS Code (agent mode) as my main teammate on this project. I attached `app.py` and `logic_utils.py` so it could see how the UI and logic related, and I started a fresh chat per bug to keep it focused.

**A correct suggestion:** The AI suggested refactoring `check_guess` and `parse_guess` out of `app.py` into `logic_utils.py`, and while moving `check_guess` it identified that the high/low hint messages were swapped (too high was telling me to "Go HIGHER"). I verified this two ways: I wrote pytest tests asserting that a too-high guess returns a message containing "LOWER" and a too-low guess returns "HIGHER" — all 6 tests passed — and I ran the game and confirmed the hints now point the right way.

**An incorrect/misleading suggestion:** When I first hit `No module named streamlit`, the AI's initial instinct was to just run `pip install -r requirements.txt`. That was misleading because the real problem was that my virtual environment had been built on the wrong Python (Xcode's 3.9) and conda's `base` was also active, so installs were landing in the wrong place. I verified this by checking `ls -la venv/bin/python*`, which showed the venv symlinked to Xcode's Python; the actual fix was to delete the venv and recreate it on Homebrew's Python 3.13 before installing.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed only when I could both (a) see the correct behavior in the live game and (b) back it with a passing automated test, so I knew it wouldn't quietly break again. Because I refactored the logic into `logic_utils.py`, the functions had no Streamlit dependency and were easy to test in isolation.

The main test I ran was `pytest` against `tests/test_game_logic.py`. It showed two useful things. First, the three starter tests were actually written wrong — they compared `check_guess(...)` to a plain string like `"Win"`, but the function returns a `(outcome, message)` tuple, so they would always fail; I fixed them to unpack the tuple. Second, my new tests for the reversed-hint bug (`"LOWER"`/`"HIGHER"` in the message) and the win bug (`check_guess(42, 42)` returns "Win") confirmed those fixes — all 6 tests passed. The AI helped me design these tests by suggesting I assert on the *direction word* in the hint rather than the whole emoji string, which made the tests less brittle. I also manually ran `streamlit run app.py` to confirm the hints, the win, and the New Game reset all worked in the real UI.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I'd say Streamlit re-runs your entire script from top to bottom every single time the user interacts with the app — clicking a button, typing in a box, anything. So any normal Python variable gets recreated from scratch on every interaction, which means it can't "remember" anything between clicks. `st.session_state` is the fix: it's a dictionary that survives those reruns, so it's where you store things you want to persist, like the secret number, the score, and whether the game is won or lost. This project drove that home through Bug #3: clicking "New Game" reset some session state keys but forgot `status`, so even though the script re-ran, the leftover "won"/"lost" value kept blocking play. The lesson is that with reruns, *what you choose to put in (and reset in) session state* is the actual game state.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**A habit I want to reuse:** separating pure logic from the UI and writing small pytest tests against it. Once I moved `check_guess` into `logic_utils.py`, I could test the exact behavior (`check_guess(42, 42)` must win) without launching Streamlit, and those tests gave me confidence the bug was actually gone and would stay gone. I want to write a quick test the moment I fix a bug from now on.

**What I'd do differently:** I'd verify the AI's environment advice before acting on it. When I hit "No module named streamlit," I almost blindly re-ran `pip install`, but the real problem was my virtual environment being built on the wrong Python interpreter. Next time I'll check *which* Python and which environment is active first, instead of assuming the AI's first suggestion is the root cause.

**How this changed my thinking:** I now treat AI-generated code as a confident first draft, not a finished product — it produced code that looked clean and "production-ready" but was full of subtle logic bugs, so it needs the same reading, testing, and skepticism I'd apply to any human-written code. Being willing to reject a suggestion (like the quick pip-install fix, or the broken starter tests that compared a tuple to a string) is part of staying in control of the process.
