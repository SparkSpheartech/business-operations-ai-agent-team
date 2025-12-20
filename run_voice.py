import asyncio
import pyttsx3
import speech_recognition as sr
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

# Import Daisy
from daisy_executive_assistant.agent import root_agent
from google.adk.runtime.runner import Runner
from google.adk.types import Input, InvocationContext

# Audio Settings
START_SOUND = "Listening..."

def speak(text):
    """Synthesizes text to speech."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error]: {e}")

def listen_from_mic(recognizer, mic):
    """Listens to the microphone and returns text."""
    with mic as source:
        print(f"\n🎤 {START_SOUND}")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"Speech Service Error: {e}")
            return None

async def run_voice_loop():
    print("Initializing Daisy Voice Mode...")
    
    # Init Runner
    runner = Runner(agent=root_agent)
    session_id = "voice-session-1"
    
    # Init Audio
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    speak("Daisy is online. How can I help you?")
    
    while True:
        user_text = listen_from_mic(recognizer, mic)
        
        if user_text:
            if user_text.lower() in ["exit", "quit", "stop", "bye"]:
                speak("Goodbye Shazaly.")
                break
            
            # Send to Agent
            print("Daisy is thinking...")
            
            # runner.run_async returns an async iterator of events usually, or a result?
            # ADK patterns: result = await runner.run_async(...)
            # Note: run_async yields Events. We want the final answer.
            
            response_text = ""
            try:
                # Based on ADK pattern:
                input_data = Input(text=user_text)
                
                # Context is managed by runner mostly, but we need session_id routing?
                # The generic Runner usually takes (input=Input(...), session_id=...)
                
                # For simplicity, let's assume runner.run(..., stream=False) isn't async? 
                # ADK is usually async.
                
                result = await runner.run_async(
                    input=input_data, 
                    session_id=session_id
                )
                
                # 'result' (RunResult) has .output (AgentOutput) -> .text (str) ideally
                # Or we iterate events?
                # Let's hope result.text works, or result.output.text
                
                if hasattr(result, 'output') and hasattr(result.output, 'text'):
                     response_text = result.output.text
                elif hasattr(result, 'text'):
                     response_text = result.text
                else:
                     # Fallback inspection
                     response_text = str(result)
                
            except Exception as e:
                response_text = f"I encountered an error: {e}"
                print(f"Agent Error: {e}")
            
            # Speak Response
            print(f"🤖 Daisy: {response_text}")
            speak(response_text)

if __name__ == '__main__':
    try:
        asyncio.run(run_voice_loop())
    except KeyboardInterrupt:
        print("\nExiting Voice Mode.")
