from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import datetime
import wikipedia
import os
import random
import pyautogui
import pyjokes
import threading
import sys

app = Flask(__name__)
CORS(app)

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    """Convert text to speech in a separate thread to avoid blocking."""
    def run_speech():
        engine.say(text)
        engine.runAndWait()

    # Start the speech synthesis in a separate thread
    thread = threading.Thread(target=run_speech)
    thread.start()

def get_time():
    """Return the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    return f"The current time is {current_time}."

def get_date():
    """Return the current date."""
    now = datetime.datetime.now()
    return f"The current date is {now.day} {now.strftime('%B')} {now.year}."

def take_screenshot():
    """Take and save a screenshot."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    return f"Screenshot saved as {img_path}."

def play_music(song_name=None):
    """Play a song from the user's Music directory."""
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        return f"Playing {song}."
    return "No song found."

def search_wikipedia(query):
    """Search Wikipedia and return a summary."""
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError:
        return "Multiple results found. Please be more specific."
    except Exception:
        return "I couldn't find anything on Wikipedia."

def shutdown():
    """Shuts down the Flask server."""
    speak("Shutting down, goodbye!")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/command", methods=["GET", "POST"])
def process_command():
    if request.method == "GET":
        # You can send a message when accessing the page via GET request
        return jsonify({"response": "Welcome to the Voice Assistant API!"})

    if request.method == "POST":
        data = request.json
        command = data.get("command")
        
        if not command:
            return jsonify({"response": "No command received."})
        
        command = command.lower()

        # Command processing
        if "what is the current time" in command:
            response = get_time()
        elif "what is the date" in command:
            response = get_date()
        elif "tell me a joke" in command:
            response = pyjokes.get_joke()
        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").strip()
            response = search_wikipedia(query)
        elif "take a screenshot" in command:
            response = take_screenshot()
        elif "play some music" in command:
            song_name = command.replace("play music", "").strip()
            response = play_music(song_name)
        elif "change your name" in command:
            response = "Name change is not implemented in this Flask version."
        elif "exit" in command:  # Add the exit command here
            shutdown()
            return jsonify({"response": "Shutting down the server."})
        else:
            response = "Command not recognized."
        
        # Speak the response (backend side)
        speak(response)
        
        # Return the response as JSON
        return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
