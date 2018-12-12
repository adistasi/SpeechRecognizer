#PROOF OF CONCEPT WITH EVERYTHING THERE

import speech_recognition as sr

currentLanguage = 'fr-FR' #British English (American English apparently accepts Spanish as input)
candidateLanguages = ['de-DE', 'es-DO', 'en-GB', 'it-IT'] #German, Spanish (Dominican Republic), French, Italian
lastThreeConfidences = [-1.0, -1.0, -1.0]
MIMIMUM_ACCEPTABLE_CONFIDENCE = .98
mostRecentAudio = None

def validateRecognizerAndMicrophone(recognizerObject, micObject):
    if not isinstance(recognizerObject, sr.Recognizer):
        raise TypeError("Recognizer variable must be of type 'Recognizer'")

    if not isinstance(micObject, sr.Microphone):
        raise TypeError("Mic variable must be of type 'Microphone'")


def sampleMicrophoneAudio(mic, recognizer, lang):
    global mostRecentAudio

    try:
        print "Please speak into the microphone for a text transcription:\n"
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            mostRecentAudio = audio
            return recognizer.recognize_google(audio, language=lang, show_all=True)
    except:
        return "Unable to generate any transcription for that utterance\n"

def updateConfidences(conf):
    lastThreeConfidences.insert(0, conf)
    lastThreeConfidences.pop()
    print lastThreeConfidences

def calculateRecentConfidence():
    return sum(lastThreeConfidences)/float(len(lastThreeConfidences))

def predictLanguage(transcription):
    return 'fr-FR'

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    validateRecognizerAndMicrophone(recognizer, mic)

    while True:
        transcription = sampleMicrophoneAudio(mic, recognizer, currentLanguage)

        if isinstance(transcription, dict) and 'alternative' in transcription.keys():
            highestConfidence = (transcription['alternative'])[0]
            updateConfidences(highestConfidence["confidence"])
            print("{} - (Confidence: {}%)".format(highestConfidence["transcript"], str(highestConfidence["confidence"] * 100)))

            if calculateRecentConfidence() < MIMIMUM_ACCEPTABLE_CONFIDENCE and -1 not in lastThreeConfidences:
                print "Recent Average Confidence too low - switching languages"
                try:
                    transcribedText = recognizer.recognize_google(mostRecentAudio)
                    # currentLanguage = predictLanguage(transcribedText)
                except:
                    print "An error occured switching languages"
        else:
            updateConfidences(0.0)
            print transcription