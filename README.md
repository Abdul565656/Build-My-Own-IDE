# DevCLI Voice Agent

DevCLI is an intelligent, never-sleeping junior developer agent that can read, write, and delete files, run shell commands, and interact with your project directory using both text and voice input. Powered by Gemini API (OpenAI-compatible), it acts as your autonomous CLI software engineer.

## Features
- **Intelligent agent**: Thinks step by step, explains reasoning, and reflects after actions.
- **File operations**: Read, write, list, and delete files safely within your project directory.
- **Shell commands**: Run terminal commands and get output.
- **Voice and text input**: Interact via typing or your microphone (requires `speech_recognition` and TTS support).
- **Cross-platform**: Works on Windows, macOS, and Linux.
- **Error handling**: Gracefully reports API errors and other issues.

## Requirements
- Python 3.8+
- [Gemini API key](https://ai.google.dev/gemini-api/docs/get-api-key) (set as `GEMINI_API_KEY` in a `.env` file)
- Packages: `openai`, `python-dotenv`, `speechrecognition`, `pyttsx3` (for TTS), and any dependencies in `pyproject.toml`

## Setup
1. **Clone the repository** and navigate to the project directory.
2. **Create a `.env` file** in the root with your Gemini API key:
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   # or, if using pyproject.toml:
   pip install .
   ```
4. **Run the agent**:
   ```sh
   python main.py
   ```

## Usage
- When prompted, choose to type your request or use your voice (if supported).
- Example requests:
  - "List all files in the project."
  - "Read the contents of main.py."
  - "Delete index.html."
  - "Run 'pip list' in the terminal."
- The agent will explain its reasoning, perform the action, and reflect on the result.

## Notes
- **API Quotas**: The Gemini API has daily free tier limits. See [Gemini API Quotas](https://ai.google.dev/gemini-api/docs/rate-limits).
- **Security**: The agent restricts file operations to the project directory for safety.
- **Voice features**: Require a working microphone and compatible TTS engine.

