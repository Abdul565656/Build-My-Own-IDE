from dotenv import load_dotenv
import os
import subprocess
import speech_recognition as sr
import pyttsx3
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    Agent,
    Runner,
    function_tool
)

# Load API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

# Setup Gemini via OpenAI compatibility
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Base directory protection
BASE_DIR = os.getcwd()

# ------------- TOOLS -------------

@function_tool
def read_file(path: str) -> str:
    full_path = os.path.abspath(path)
    if not full_path.startswith(BASE_DIR):
        return "Access denied."
    with open(full_path, 'r') as f:
        return f.read()

@function_tool
def write_file(path: str, content: str) -> str:
    full_path = os.path.abspath(path)
    if not full_path.startswith(BASE_DIR):
        return "Access denied."
    with open(full_path, 'w') as f:
        f.write(content)
    return f"{path} has been written."

@function_tool
def delete_file(path: str) -> str:
    full_path = os.path.abspath(path)
    if not full_path.startswith(BASE_DIR):
        return "Access denied."
    if not os.path.exists(full_path):
        return f"{path} does not exist."
    try:
        os.remove(full_path)
        return f"{path} has been deleted."
    except Exception as e:
        return f"Error deleting {path}: {str(e)}"

@function_tool
def list_files(dir_path: str = ".") -> list[str]:
    full_dir = os.path.abspath(dir_path)
    if not full_dir.startswith(BASE_DIR):
        return ["Access denied."]
    file_list = []
    for root, _, files in os.walk(full_dir):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), BASE_DIR))
    return file_list

@function_tool
def run_command(command: str) -> str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error running command: {str(e)}"

# ------------- VOICE SETUP -------------

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 170)

def listen_to_voice() -> str:
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech recognition error."

def speak(text: str):
    print("\n🔊 Speaking:")
    print(text)
    tts_engine.say(text)
    tts_engine.runAndWait()

# ------------- AGENT -------------

agent = Agent(
    name='DevCLI',
    instructions="""
    You are DevCLI, an intelligent junior developer who never sleeps.
    - You always think step by step before taking action.
    - You explain your reasoning and what you plan to do before you do it.
    - You are curious, careful, and eager to learn.
    - After each action, reflect on what you did and how it could improve.
    - Narrate your thought process as you work.
    - You have full control over the project directory: you can read/write/delete files, run shell commands, and list directories.
    """,
    tools=[read_file, write_file, delete_file, list_files, run_command]
)

# ------------- MAIN LOOP -------------

if __name__ == "__main__":
    print("🤖 DevCLI Voice Agent Ready!")

    while True:
        choice = input("\n🎧 Choose input mode — (t)ype or (v)oice or 'exit': ").strip().lower()

        if choice in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if choice == "v":
            task = listen_to_voice()
        else:
            task = input("\n💬 Type your request: ")

        if not task.strip():
            continue

        try:
            result = Runner.run_sync(agent, task, run_config=config)
            print("\n🧠 AI Agent Output:\n")
            print(result.final_output)
            speak(result.final_output)
        except Exception as e:
            error_msg = f"Sorry, there was an error: {e}"
            print(f"\n❗ Error: {e}")
            speak(error_msg)
