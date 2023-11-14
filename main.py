import g4f
import speech_recognition as sr
from googletrans import Translator
import asyncio
import pyttsx3 as tts

engine = tts.init()
voices = engine.getProperty('voices')

_providers = [
    g4f.Provider.GptGo,
]

r = sr.Recognizer()
translator = Translator()

#Georgian Language
def RunGeorgianTTS():
    isRunning = True
    while isRunning == True:
        engine.setProperty('voice', voices[2].id)
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            print("Speak...")
            audio_data = r.listen(source)
            print("Recognizing...")

            try:
                # convert speech to text
                response = r.recognize_google(audio_data, show_all=False, language="ka_GE")
                print(response)
                if response == "გაჩერდი":
                    isRunning = False
                output = translator.translate(response, dest="en")

                async def run_provider(provider: g4f.Provider.BaseProvider):
                    try:
                        response = await g4f.ChatCompletion.create_async(
                            model=g4f.models.default,
                            messages=[{"role": "user", "content": output.text}],
                            provider=provider,
                        )
                        result = translator.translate(response, dest="ka")
                        engine.say(result.text)
                        engine.runAndWait()
                        engine.stop()
                    except Exception as e:
                        print(e)


                async def run_all():
                    calls = [
                        run_provider(provider) for provider in _providers
                    ]
                    await asyncio.gather(*calls)


                asyncio.run(run_all())

            except:
                print(None)

#English Language
def RunEnglishTTS():
    isRunning = True
    while isRunning == True:
        engine.setProperty('voice', voices[0].id)
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            print("Speak...")
            audio_data = r.listen(source)
            print("Recognizing...")

            try:
                response = r.recognize_google(audio_data, show_all=False, language="en-US")
                print(response)
                if response == "stop":
                    isRunning = False
                output = response
                async def run_provider(provider: g4f.Provider.BaseProvider):
                    try:
                        response = await g4f.ChatCompletion.create_async(
                            model=g4f.models.default,
                            messages=[{"role": "user", "content": output}],
                            provider=provider,
                        )
                        engine.say(response)
                        engine.runAndWait()
                        engine.stop()
                    except Exception as e:
                        print(e)


                async def run_all():
                    calls = [
                        run_provider(provider) for provider in _providers
                    ]
                    await asyncio.gather(*calls)


                asyncio.run(run_all())

            except:
                pass

print("Choose your language (English | Georgian)")
Language = input(": ")
if Language == "english":
    RunEnglishTTS()
elif Language == "georgian":
    RunGeorgianTTS()
