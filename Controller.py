# Bring in References to the Python SpeechRecognition Library and our Language Prediction (Machine Learning) System
import speech_recognition as sr
import LanguagePrediction as lp

# Create 'class objects'
controllerRecognizer = sr.Recognizer()  # Create a special language-agnostic recognizer for the controller (so we don't have to deal with classifying audio)
lastThreeConfidences = [-1.0, -1.0, -1.0]  # Create an array to monitor the 3 most recent confidences
MIMIMUM_ACCEPTABLE_CONFIDENCE = .98  # Define a minimum acceptable confidence for the application

'''
Function to monitor the results of the system and update our average confidence every time we get a new recording
    @param newConfidence The most recent confidence of the system
'''
def monitor(newConfidence):
    print("=====MONITOR=====")
    # Add newest confidence to the beginning of the array and remove the oldest confidence
    lastThreeConfidences.insert(0, newConfidence)
    lastThreeConfidences.pop()

'''
Function to analyze our system properties to ensure we're meeting an acceptable minimum confidence
    @return Boolean indicating whether or not our average confidence is below our acceptable minumum
            (True = below minimum (BAD), False = above minimum (GOOD)) 
'''
def analyze():
    print "=====ANALYZE====="
    # Calculate the average confidence & alert the system if it's below our acceptable minimum (and no -1's in array to indicate we're past initial condition)
    averageConfidence = sum(lastThreeConfidences)/float(len(lastThreeConfidences))
    return (averageConfidence < MIMIMUM_ACCEPTABLE_CONFIDENCE and -1 not in lastThreeConfidences)

'''
Function to take in an audio transcription and identify its most likely language (so we can switch the system to that language)
    @param mostRecentAudio The most recent audio transcription
'''
def plan(mostRecentAudio):
    print "=====PLAN====="
    if analyze():  # If our analyze function indicates that we're below average confidence, we identify our new language
        print "Recent Average Confidence too low - identifying new suggested language"
        try:
            #  Using a language-agnostic recognizer, get the transcription so we can feed it into our ML Algorithm
            transcribedText = controllerRecognizer.recognize_google(mostRecentAudio)
            print transcribedText
            newLanguage = lp.predictLanguage(transcribedText)

            # Call our execute function to enact changes on the system
            return execute(newLanguage)
        except:
            # General Error handling
            print "An error occurred switching languages"

    # If we don't need to execute any changes, return nothing
    return ""

'''
Function to 'execute' the change on the system and return what we're changing
    @param newLanguage The language we're changing the system to
    @return newLanguage The language we're changing the system to
'''
def execute(newLangauge):
    print "=====EXECUTE====="
    print "Switching system to {}".format(newLangauge)
    return newLangauge