import streamlit as st
import requests
import json


#TODO: remove error screen at the start when no game is chosen

# FastAPI endpoint URL
api_url = "http://127.0.0.1:8000/prompt"  # Ensure the FastAPI app is running


# Title of the Streamlit app
st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3VwaHoyNTU1eGgxeHBjOW9qaG40ZG5tbjJ0cmkxcW1jMmVjcDhybSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3orieMvIzyjwayeK1q/giphy.gif", use_container_width=True)
st.title("🎲🎲🎲 Do you need help with a game 🎲🎲🎲?")
st.title("Welcome 7 Wonders - the place where you find all your answers")
st.snow()

# List of games
with open("games.json", "r") as f:
    games_list = json.loads(f.read())

#games_list = ["kingdomino", "battle sheep", "dr eureka", "codenames", "when i dream", "unlock escape adventures", "terraforming mars", "seven wonders duel", "exploding kittens", "this war of mine the board game", "queendomino", "7 wonders", "catan"]


# Dynamic game suggestion input
st.text("Start typing the game you are playing:")
game_input = st.text_input("Game Name")

filtered_games = None
# Filter the game dynamically
if game_input:
    filtered_games = [game for game in games_list if game_input.lower() in game.lower()]
else:
    filtered_games = st.selectbox("Select the game from the suggestions:",game_input)


#Show filtered games in a dropdown
if filtered_games:
    selected_game = st.selectbox("Select the game from the suggestions:", filtered_games)

# Create a form to handle submission with the Enter key
    with st.form(key="query_form"):
        # Prompt text box for user input
        st.text("What do you need to know?")
        user_input = st.text_input("")

        # Submit button
        submit_button = st.form_submit_button("Enter")

        if submit_button:
            if user_input:
                # Send request to FastAPI
                with st.spinner("Finding the perfect answer for you..."): # this creates a loading animation
                    try:
                        response = requests.get(
                            api_url,
                            params={"query": user_input, "game": selected_game},
                            timeout=60
                            )

                        if response.status_code == 200:
                            # Parse the JSON response
                            response_data = response.json()
                            # Display the answer from FastAPI
                            answer = response_data.get("answer", "No answer provided.")[0]["generated_text"]
                            dist = response_data.get("distance")

                            if min(dist) <= 0.8:
                                st.balloons()
                                st.write(answer)

                            else:
                                st.write("Im dumb")

                        else:
                            st.write("Error: Could not retrieve answer from the API.")
                    except Exception as e:
                            st.error(f"An error occurred: {e}")
            else:
                st.write("Please enter a question.")

else:
    st.warning("No matching game found. Please try typing a different name.")
    selected_game = None # Ensure no game is selected if none match
