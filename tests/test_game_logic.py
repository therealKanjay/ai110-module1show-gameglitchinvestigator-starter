"""Regression tests targeting the specific bugs fixed in game.py.

Each test maps to a "Collab fix" documented in game.py and asserts the
*corrected* behavior, so it would fail against the original glitchy code.
"""
import os
import sys

# Make the repo root importable when pytest runs from inside tests/.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random

from game import (
    GameState,
    apply_guess,
    check_guess,
    get_range_for_difficulty,
    new_game,
    update_score,
)


# Bug 1: "Hard" used a smaller range than "Normal" (harder was easier).
# Fix: Hard is now 1-200 so the range grows with difficulty.
def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert get_range_for_difficulty("Hard") == (1, 200)
    assert hard_high > normal_high


# Bug 2: Hints pointed the wrong way (too-high told you to go HIGHER).
# Fix: Too High -> go LOWER, Too Low -> go HIGHER.
def test_check_guess_hint_directions():
    assert check_guess(50, 50) == ("Win", "🎉 Correct!")

    outcome, message = check_guess(80, 50)  # guess above secret
    assert outcome == "Too High"
    assert "LOWER" in message

    outcome, message = check_guess(20, 50)  # guess below secret
    assert outcome == "Too Low"
    assert "HIGHER" in message


# Bug 3: Off-by-one docked points for a first-try win (used attempt_number + 1).
# Fix: a 1st-attempt win earns the full 100 (uses attempt_number - 1).
def test_first_try_win_earns_full_points():
    assert update_score(0, "Win", 1) == 100
    # Each later attempt costs 10 points.
    assert update_score(0, "Win", 2) == 90
    # Points floor out at 10, never lower.
    assert update_score(0, "Win", 99) == 10


# Bug 4: "Too High" used to ADD points on some attempts (rewarding a wrong guess).
# Fix: both wrong outcomes consistently subtract 5.
def test_wrong_guesses_always_subtract_five():
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95
    assert update_score(100, "Too Low", 2) == 95
    assert update_score(100, "Too Low", 3) == 95


# Bug 5: "New Game" reused a 1-100 secret and kept stale score/attempts/history.
# Fix: new_game builds a fresh GameState from the actual range every time.
def test_new_game_resets_state_and_respects_range():
    state = new_game(1, 20, rng=random.Random(0))
    assert state.attempts == 0
    assert state.score == 0
    assert state.status == "playing"
    assert state.history == []
    assert 1 <= state.secret <= 20


# Bug 6: The secret was flipped to a string on alternating turns, silently
# breaking comparisons. Fix: always compare against the real int secret.
def test_secret_comparison_stable_across_turns():
    state = GameState(secret=42)
    # Several wrong turns in a row must all report consistently — no
    # alternating-turn glitch where a correct-direction guess flips.
    _, r1 = apply_guess(state, "10", attempt_limit=8)
    _, r2 = apply_guess(state, "11", attempt_limit=8)
    _, r3 = apply_guess(state, "12", attempt_limit=8)
    assert r1.outcome == "Too Low"
    assert r2.outcome == "Too Low"
    assert r3.outcome == "Too Low"

    # And the matching int guess still wins on a later turn.
    _, win = apply_guess(state, "42", attempt_limit=8)
    assert win.outcome == "Win"
    assert win.won is True
    assert state.status == "won"
