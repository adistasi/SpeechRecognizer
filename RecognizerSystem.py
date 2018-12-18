# Bring in References to the Python SpeechRecognition Library and our Autonomous Controller
import speech_recognition as sr
import Controller as cont

# Define 'class' variables to save current language and the most recent audio input
currentLanguage = 'en-GB'  # British English (American English apparently accepts Spanish as input)
candidateLanguages = ['de-DE', 'es-DO', 'fr-FR', 'it-IT']  # German, Spanish (Dominican Republic), French, Italian
mostRecentAudio = None

'''
Simple function to validate that the recognizer and microphone objects are of the correct type\
    @param recognizerObject The sr.Recognizer object we're validating
    @param micObject The sr.Microphone object we're validating
    @return Raises a TypeError if either variable is an inappropriate type
'''
def validateRecognizerAndMicrophone(recognizerObject, micObject):
    if not isinstance(recognizerObject, sr.Recognizer):
        raise TypeError("Recognizer variable must be of type 'Recognizer'")

    if not isinstance(micObject, sr.Microphone):
        raise TypeError("Mic variable must be of type 'Microphone'")


'''
Function to accept audio input from a microphone and pass it into the recognizer object for transcription
    @param mic The sr.Microphone object (The system's default microphone)
    @param recognizer The sr.Recognizer object that we're using to transcribe audio
    @param lang The specified language of the system (can be English, French, German, Spanish, or Italian)
    @return Either the transcription object or a string indicating an error
'''
def sampleMicrophoneAudio(mic, recognizer, lang):
    # Use the global keyword so we can update the 'mostRecentAudio' state variable
    global mostRecentAudio

    try:  # Try to handle UnknownValueError generated when the system can't generate a transcription (doesn't recognize)
        print "=========================================================="
        print "Please speak into the microphone for a text transcription:\n"
        with mic as source:  # Sample audio from microhpone
            #  Use first .5 seconds of audio to filter out & ignore ambient noise - raises transcription confidence
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            mostRecentAudio = audio  # Update saved most recent audio

            # return recognizer result, with show_all=True, this includes transcription & confidence, with possible alternate transcriptions
            return recognizer.recognize_google(audio, language=lang, show_all=True)
    except:
        return "Unable to generate any transcription for that utterance\n"



if __name__ == "__main__":
    global currentLanguage  # Ensure we're updating the system's currentLanguage variable instead of a local variable

    # Create Recognizer & Mic to sample audio
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    validateRecognizerAndMicrophone(recognizer, mic)  # Ensure recognizer & mic are valid

    while True:  # Continuously loop through asking for a transcription
        try:
            transcription = sampleMicrophoneAudio(mic, recognizer, currentLanguage)
            # Get transcription and check that it's in the expected format
            if isinstance(transcription, dict) and 'alternative' in transcription.keys():
                # Print the results (in lieu of actually doing something with the transcription)
                highestConfidence = (transcription['alternative'])[0]
                print("{} - (Confidence: {}%)".format(highestConfidence["transcript"].encode('utf-8'), str(highestConfidence["confidence"] * 100)))

                # Autonomous Controller hooks - allows the system to monitor, analyze, plan, & execute on the system
                cont.monitor(highestConfidence["confidence"])
                result = cont.plan(mostRecentAudio)

                if result != "":
                    currentLanguage = result
            else:
                # If we didn't get a valid transcription, send a 0 for the confidence to the controller and reprompt
                cont.monitor(0.0)
                print transcription
        except:
            # General error handling to ensure the application doesn't stop on an error
            print "Some error has occured during the transcription process"
