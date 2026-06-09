from logic_utils import check_guess

# check_guess returns a (outcome, message) tuple, so we unpack it.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug #1: hint direction must NOT be reversed ---

def test_too_high_hint_tells_player_to_go_lower():
    # A guess that is too high should tell the player to go LOWER
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_tells_player_to_go_higher():
    # A guess that is too low should tell the player to go HIGHER
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- Bug #2: a correct integer guess always wins (no string coercion) ---

def test_correct_int_guess_always_wins():
    # 42 == 42 must be a Win; the old bug compared 42 to "42" and missed it
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"
