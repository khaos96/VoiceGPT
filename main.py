from os import system
from EdgeGPT.EdgeUtils import Query
import speech_recognition as sr
import sys, whisper, warnings, time, openai

# Initialize the OpenAI API
openai.api_key = ""

r = sr.Recognizer()
base_model = whisper.load_model('base')
source = sr.Microphone() 
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()
from os import system
from EdgeGPT.EdgeUtils import Query
import speech_recognition as sr
import sys, whisper, warnings, time, openai

# Initialize the OpenAI API
openai.api_key = "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"

r = sr.Recognizer()
base_model = whisper.load_model('base')
source = sr.Microphone() 
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def prompt_gpt():
    while True:
        try:
            print("Processing GPT prompt...")
            with source as s:
                r.adjust_for_ambient_noise(s, duration=2)
                audio = r.listen(s)
            with open("prompt.wav", "wb") as f:
                f.write(audio.get_wav_data())
            result = base_model.transcribe('prompt.wav')
            prompt_text = result['text']
            print(f"USER: {prompt_text.strip()}")
            if len(prompt_text.strip()) == 0:
                print("Empty prompt. Please speak again.")
                speak("Empty prompt. Please speak again.")
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt_text},
                    ],
                    temperature=0.5,
                    max_tokens=100,
                    top_p=0.9,
                    frequency_penalty=0,
                    presence_penalty=0,
                    n=1,
                    stop=["\nUser:"],
                )
                bot_response = response["choices"][0]["message"]["content"]
                print('GPT: ' + bot_response)
                speak(bot_response)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Prompt error: ", e)

if __name__ == '__main__':
    prompt_gpt()