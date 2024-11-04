import streamlit as st
import random

st.markdown("""
    <style>
        .game-title {color: #FF6347; font-size: 40px; font-weight: bold; text-align: center; margin-bottom: 20px;}
        .rules {font-size: 18px; color: #f0f8ff; padding: 10px; border-radius: 10px; margin: 20px 0;}
        .result {font-size: 22px; font-weight: bold; color: #228B22;}
        .higher-lower {color: #FF4500; font-weight: bold;}
        .user-name {color: red; font-weight: bold; font-size: 25px} 
        .txt{color:yellow ; font-weight :bold; font-size: 20px}
        .lost{color:red ;font-weight :bold ;font-size:18px}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='game-title'>Welcome to the Guessing Game!</div>", unsafe_allow_html=True)

if 'guessing_num' not in st.session_state:
    st.session_state.guessing_num = random.randint(1, 50)
    st.session_state.attempts = 0
    st.session_state.machine_attempts = 0
    st.session_state.game_over = False
    st.session_state.name = ""
    st.session_state.machine_low = None
    st.session_state.machine_high = None
    st.session_state.machine_guess = None
    st.session_state.machine_game_over = False
    st.session_state.temp=0
    st.session_state.sub=False

if not st.session_state.name:
    st.session_state.name = st.text_input("Enter your name:")
    if st.button("Submit"):
        st.session_state.temp=1


tab1, tab2 = st.tabs(["PLAYER GUESS", "MACHINE GUESS"])
with tab1:
    st.header("Machine thinks a Number, User Guesses")
    st.write("""
        <div class='rules'>
            <strong>Rules:</strong><br>
            The computer has chosen a random number between 1 and 50.<br>
            Try to guess the number! You’ll receive hints of "higher" or "lower" based on your input.<br>
            The game keeps track of your attempts. Good luck!
        </div>
    """, unsafe_allow_html=True)
    if not st.session_state.name:
        st.write("<div class='user-name'>Enter your name to continue</div>", unsafe_allow_html=True)
    if st.session_state.name:
        st.write(f"<div class='txt'>Welcome, {st.session_state.name}! Let's start the game!</div>",unsafe_allow_html=True)
        guess = st.number_input("Enter your guess:", min_value=1, max_value=50, step=1)

        if st.button("Submit Guess") and not st.session_state.game_over:
            st.session_state.attempts += 1

            if st.session_state.attempts>=3:
                st.write("<div class='lost'>Sorry you lost!(attempted 15 times) </div>",  unsafe_allow_html=True)
                st.header(f"The Machine guessed {st.session_state.guessing_num}")
                st.session_state.game_over = False
            elif guess < st.session_state.guessing_num:
                st.write("<div class='higher-lower'>Try a higher number!</div>", unsafe_allow_html=True)
            elif guess > st.session_state.guessing_num:
                st.write("<div class='higher-lower'>Try a lower number!</div>", unsafe_allow_html=True)
            else:
                st.write(f"<div class='result'>Congratulations, {st.session_state.name}! You guessed it in {st.session_state.attempts} attempts!</div>", unsafe_allow_html=True)
                st.session_state.game_over = True

        if st.button("Restart Game"):
            st.session_state.guessing_num = random.randint(1, 50)
            st.session_state.attempts = 0
            st.session_state.game_over = False
            st.write("Game restarted! Try to guess the new number.")

with tab2:
    st.header("User Thinks a Number, Machine Guesses")
    st.write("""
        <div class='rules'>
            <strong>Rules:</strong><br>
            You think of a number within a given range, and the computer will try to guess it using binary search.<br>
            Provide hints by entering "1" if the guess is too low, "0" if it's too high, or "2" if the guess is correct.<br>
            Good luck!
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.name:
        st.write("<div class='user-name'>Enter your name to continue</div>", unsafe_allow_html=True)
    elif st.session_state.name:
        st.write(f"<div class='txt'>Welcome, {st.session_state.name}! Let's start the game!</div>", unsafe_allow_html=True)
        if not st.session_state.sub:
            st.session_state.machine_low = st.number_input("Enter the starting range", step=1)
            st.session_state.machine_high = st.number_input("Enter the ending range", step=1)
            st.session_state.machine_attempts = 0
            if st.button("Start machine guess"):
                st.session_state.sub=True

        if  st.session_state.machine_high > st.session_state.machine_low:
                st.session_state.sub=True
                st.session_state.machine_guess = (st.session_state.machine_low + st.session_state.machine_high) // 2
                st.write(f"Machine's first guess: {st.session_state.machine_guess}")

        if st.session_state.machine_guess is not None:
            hint = st.selectbox("Hint: your value is high (1), low (0), or correct (2)?", [1, 0, 2])

            if st.button("Enter the choice"):
                st.session_state.machine_attempts += 1
                if hint == 1:
                    st.session_state.machine_low = st.session_state.machine_guess + 1
                elif hint == 0:
                    st.session_state.machine_high = st.session_state.machine_guess - 1
                elif hint == 2:
                    st.write(f"<div class='result'>Hurray! The machine guessed your number: {st.session_state.machine_guess} in {st.session_state.machine_attempts} attempts</div>", unsafe_allow_html=True)
                    st.session_state.machine_game_over = True

                if not st.session_state.machine_game_over:
                    if st.session_state.machine_low <= st.session_state.machine_high:
                        st.session_state.machine_guess = (st.session_state.machine_low + st.session_state.machine_high) // 2
                        st.write(f"Machine's next guess: {st.session_state.machine_guess}")
                    else:
                        st.error("Inconsistent hints given; no possible numbers left in the range.")

        if st.button("Restart Machine Game"):
            st.session_state.machine_low = None
            st.session_state.machine_high = None
            st.session_state.machine_guess = None
            st.session_state.machine_attempts = 0
            st.session_state.sub=False
            st.session_state.machine_game_over = False
            st.write("Game restarted! Think of a new number.")