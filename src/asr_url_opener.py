
import sys
import webbrowser as web
import speech_recognition as sr
CHROME_PATH = '/usr/bin/google-chrome %s'

import warnings; warnings.simplefilter('ignore')

def open_url(url):
    web.get(CHROME_PATH).open(url)

def text_to_command(text):
    print(f"Recognized: {text}")
    if text.startswith("open url"):
        url = text.replace("open url", "")
        open_url(url)
    if text == 'exit':
        print("Exiting")
        sys.exit()
        
    
def main_loop():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                r.adjust_for_ambient_noise(mic, duration=0.2)
                audio = r.listen(mic)
                text = r.recognize_google(audio)
                text = text.lower()
                text_to_command(text)
                
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            continue
        except KeyboardInterrupt:
            print("Exiting main loop")
            break
        except Exception as e:
            print(e)
            recognizer = sr.Recognizer()
            continue
    
if __name__ == '__main__':
    main_loop()
    
