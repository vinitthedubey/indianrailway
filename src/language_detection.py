import playsound
import sounddevice as sd
import wavio
import pyttsx3






def record_audio(duration, filename):
    # Record audio
    fs = 44100  # Sampling frequency
    print("starting........")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save audio to file
    wavio.write(filename, recording, fs, sampwidth=2)



    
import speech_recognition as sr

def audio_to_text(filename):
    recognizer = sr.Recognizer()

    # Load audio file
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    # Recognize speech using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data, language='en-US')
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def Run():
    arr=["data/hindif_option.mp3","data/englishf_option.mp3","data/marathif_option.mp3","data/bengalif_option.mp3","data/russianf_option.mp3","data/spanishf_option.mp3","data/teluguf_option.mp3","data/tamilf_option.mp3"]

    for i in arr:
        playsound.playsound(i)

    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # Ask user to select preferred language
    engine.say("Select your preferred language.")
    engine.runAndWait()

    # Record audio
    duration = 4  # Duration of recording in seconds
    filename = "test" + ".wav"
    record_audio(duration, filename)

    filename = "test.wav"
    text = audio_to_text(filename)
    return text
