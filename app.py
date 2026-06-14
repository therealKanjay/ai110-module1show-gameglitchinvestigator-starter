import streamlit as st

import game


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = game.get_attempt_limit(difficulty)
low, high = game.get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "game" not in st.session_state:
    st.session_state.game = game.new_game(low, high)

state = st.session_state.game

st.subheader("Make a guess")

# Collab fix: this prompt was hardcoded to "between 1 and 100" regardless of
# difficulty. Ahmed noticed it lied on Easy/Hard; Claude wired it to the real
# {low}/{high} from the selected difficulty.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", state.secret)
    st.write("Attempts:", state.attempts)
    st.write("Score:", state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.game = game.new_game(low, high)
    st.success("New game started.")
    st.rerun()

if state.status != "playing":
    if state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    state, result = game.apply_guess(state, raw_guess, attempt_limit)
    st.session_state.game = state

    if result.error:
        st.error(result.error)
    else:
        if show_hint:
            st.warning(result.message)

        if result.won:
            st.balloons()
            st.success(
                f"You won! The secret was {state.secret}. "
                f"Final score: {state.score}"
            )
        elif result.lost:
            st.error(
                f"Out of attempts! "
                f"The secret was {state.secret}. "
                f"Score: {state.score}"
            )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
