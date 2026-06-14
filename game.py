"""Pure game logic for the guessing game. No Streamlit / UI imports here."""
import random
from dataclasses import dataclass, field


# Game-rule data (not UI).
ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def get_attempt_limit(difficulty: str) -> int:
    return ATTEMPT_LIMITS[difficulty]


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


@dataclass
class GameState:
    secret: int
    attempts: int = 0
    score: int = 0
    status: str = "playing"  # "playing" | "won" | "lost"
    history: list = field(default_factory=list)


@dataclass
class TurnResult:
    outcome: str = ""
    message: str = ""
    error: str = ""
    won: bool = False
    lost: bool = False


def new_game(low: int, high: int, rng=random) -> GameState:
    """Create a fresh game state with a secret in [low, high]."""
    return GameState(secret=rng.randint(low, high))


def apply_guess(state: GameState, raw_guess: str, attempt_limit: int):
    """Apply one guess to the state. Returns (state, TurnResult). Pure of UI."""
    state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)
    if not ok:
        state.history.append(raw_guess)
        return state, TurnResult(error=err)

    state.history.append(guess_int)

    outcome, message = check_guess(guess_int, state.secret)
    state.score = update_score(state.score, outcome, state.attempts)

    result = TurnResult(outcome=outcome, message=message)

    if outcome == "Win":
        state.status = "won"
        result.won = True
    elif state.attempts >= attempt_limit:
        state.status = "lost"
        result.lost = True

    return state, result
