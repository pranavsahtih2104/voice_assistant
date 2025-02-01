import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import webbrowser
import requests
import time

# Initialize the voice engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Print available voices and their indices
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name}")

# Select a voice based on the system voices
engine.setProperty('voice', voices[0].id)  # Change the index as needed

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        print("Sorry, I didn't catch that. Could you repeat?")
        return None

# Function to perform basic math operations
def perform_math(query):
    if 'plus' in query or '+' in query:
        numbers = [int(i) for i in query.split() if i.isdigit()]
        result = sum(numbers)
        speak(f"The result is {result}")
    elif 'minus' in query or '-' in query:
        numbers = [int(i) for i in query.split() if i.isdigit()]
        result = numbers[0] - numbers[1]
        speak(f"The result is {result}")
    elif 'times' in query or 'x' in query:
        numbers = [int(i) for i in query.split() if i.isdigit()]
        result = numbers[0] * numbers[1]
        speak(f"The result is {result}")
    elif 'divided' in query or '/' in query:
        numbers = [int(i) for i in query.split() if i.isdigit()]
        if numbers[1] == 0:
            speak("Sorry, I cannot divide by zero.")
        else:
            result = numbers[0] / numbers[1]
            speak(f"The result is {result}")

# Function to get weather update
def get_weather(query):
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    query = query.replace("weather", "").strip()
    speak(f"Getting weather for {query}...")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        main = response["main"]
        weather = response["weather"][0]["description"]
        temperature = main["temp"]
        speak(f"The weather in {query} is {weather} with a temperature of {temperature}°C.")
    else:
        speak("I couldn't fetch the weather. Please try again.")

# Function to set an alarm
def set_alarm(query):
    speak("Setting alarm. Please say the time in 24-hour format, for example, 15:30.")
    alarm_time = listen()
    if alarm_time:
        alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
        while True:
            current_time = datetime.datetime.now()
            if current_time.hour == alarm_hour and current_time.minute == alarm_minute:
                speak("Time's up! Your alarm is ringing!")
                break
            time.sleep(30)  # Check every 30 seconds

# Function to respond to commands
def respond_to_query(query):
    if "hello" in query:
        speak("Hello! How can I assist you today?")
    elif "your name" in query:
        speak("I am Jarvis, your personal assistant.")
    elif "what can you do" in query:
        speak("I can answer simple math questions, weather updates, open websites, set alarm , and more. Just ask me!")
    elif "time" in query:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%H:%M')}.")
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=1)
        speak(result)
    elif "open" in query:
        query = query.replace("open", "")
        webbrowser.open(query)
        speak(f"Opening {query}")
    elif "weather" in query:
        get_weather(query)
    elif "alarm" in query:
        set_alarm(query)
    elif "goodbye" in query:
        speak("Goodbye! Have a nice day!")
        exit()
    elif "plus" in query or "minus" in query or "times" in query or "divided" in query:
        perform_math(query)

# Main loop to run the assistant
def run_assistant():
    speak("Hello, I am Jarvis. How can I assist you?")
    while True:
        query = listen()
        if query:
            respond_to_query(query)

if __name__ == "__main__":
    run_assistant()
