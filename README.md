# Speech Recognizer

## Team Members
- Andrew DiStasi
- Cervantes Hernandez
- Diosdavi Reyes

## Dependencies
 - Python 2.7
 - SpeechRecognition
 - PyAudio
 - NLTK
 - scikit-learn
 
 ## Project Overview
 Our application is a self-adaptive speech recognition system that attempts to switch languages if the utterance confidence for a given input is too low.  A controller monitors the application and tracks results over the last two speech utterances.  If the confidence is below 70% (which we identified as an acceptable industry standard), the application uses a Machine Learning classifier to attempt to classify the most likely language of the utterance and switch the SpeechRecognition language to that.
 
 To allow for runtime classification of languages, we utilize a Machine Learning model that can classify text into one of five likely languages - British English ("en-GB"), Spanish (Dominican Republic) ("es-DO"), French ("fr-FR"), German ("de-DE"), and Italian ("it-IT").  The classifier is constructed as a "majority votes" classifier composed of three individual classifiers - Bernoulli NB, Naive Bayes, and Decision Tree.  In a majority votes classifier, each classifier returns a prediction, and the most popular answer is returned as the accepted prediction.  This can help to combine the strengths and accuracies of each classifier while helping to mitigate errors based on a single classifier.  The Naive Bayes classifier is the cannonical and most popular baseline method for text classification.   In this model, word frequencies are inputted as features.  A variation of Naive Bayes, Bernoulli NB is distinct enough to warrant inclusion in our classifer without introducing bias.  In this model, which is popular for classifying short texts, the features are independent booleans.  Finally, the Decision Tree classifier buils a tree of decision points that result in classification based on inputted parameters.
 
 ## System Goals
  - The system will take in speech input and transcribe what was said in written text.
  - The system will display the confidence level for a given utterance
  - If the average confidence is below an acceptable threshold of 70% over two utterances, the system will switch to the language with the highest confidence.
 
Number | Category | Description
------ | -------- | ----------- |
1 |Goals | Average Sentence Confidence > 70% and Response Time < 3 seconds
2 | Disturbances | External Noise in Audio Transcriptions
4 | Noise | Processing overhead introduced by measurement and controller
5 | Software Model | Predictive Model to identify an utterance's language
6 | Knobs | Language Switching
 
 ## System Diagram and Control Diagram
 ![System Design Overview](http://andydistasi.com/dev/SWEN789/Overview.png)
 
 The above image shows an overall diagram of our system and controller.  These views are broken down for consideration in the following sections.
 
 ![Control Diagram](http://andydistasi.com/dev/SWEN789/Control.png)


This image shows a control diagram detailing the intended functionality of our system.  The system accepts a minimum acceptable confidence of speech utterances (70%) and works to maintain that confidence over the duration of the system.  The controller applies corrections to the system in the form of switching the language of the system (if the error is too great - i.e. the confidence is too low).  The system records and transcribes the utterance, returning the average confidence of the sentence's transcription, which is fed into the controller.  Also diagrammed are identifications of Noise and Disturbance.  The disturbance is any external noise in the audio transcriptions.  Steps are taken within the code to filter out these disturbances by sampling the first .5 seconds of a speech input and using it to identify the ambient noise and adjust the sensitivity accordingly.  The Noise (with regards to the system) is the processing overhead introduced by the confidence measurements, controller, and machine learning component. 

 ## MAPE-K Overview
 ![MAPE-K Controller](http://andydistasi.com/dev/SWEN789/MAPE.png)
 
 This image shows the MAPE-K Controller overview for the application.  The responsibilities for each section are defined as follows:
 - **Monitor** - Watch system for returned confidence levels
 - **Analyze** - Identify if our confidence levels are dipping below acceptable levels
 - **Plan** - If we are below acceptable confidence, identify a target language (with a higher confidence to switch to).  Ensure that this process doesn't not exceed some prescribed response time.
 - **Execute** - Issue commands that switch the system to the new language
 
 ## Machine Learning Dataset and Features
 Our Dataset for training our Machine Learning Model was the Europarl parallel corpus.  This corpus is a transcription of EU Parliament meetings in many different languages.  For our project, we utilized the English, French, German, Italian, and Spanish transcriptions.  Each dataset was preprocessed via tokenization, casting the text to lowercase, and removing any non-language tags.  400 lines for each corpus were extracted and labeled for a total of 2,000 lines.  360 Lines of each language were used for training (a training set of 1,800 lines) and 40 of each language were used for testing (a testing set of 200 lines).
 
 Features considered during the implementation were character bigrams, character trigrams, and average word length.  Character bigrams and trigrams are each sequential combination of 2 or 3 (respectively) characters in a word.  This information is useful because there are certain bigrams and trigrams that are very common in some languages, but not present in others.  For example, a bigram of 'el' or 'la' would be very common in Spanish texts.  A bigram of 'cj' would be less common in English.  Average word length is also valuable.  Language like German use a compound adjective system, where modifiers for a noun are appended as suffixes to a noun, whereas languages like English add additional words as modifiers.  As a result, the average word length of a German Sentence is likely to be longer than that of another language.  These features were extracted for each transcription and fed into the machine learning algorithms for classification.
 
 ## Industry Standards & Speech Recognition Considerations
  ![Confidence Graph](http://andydistasi.com/dev/SWEN789/Confidence.png)
  
 he above image shows a graph from a study on Google Speech Recognition capabilities that correlates transcription confidence to user growth.  Speech Recognition/Transcription confidence is the highest barrier to acceptance for a speech application.  Any average confidence below .7 (70%) results in usage decay, or a user growth relate below 1.  Therefore, we define 70% as our industry standard of a minimum acceptable confidence.  Response time is somewhat less critical than confidence and is more application-specific.  Certain applications may naturally lend themselves to an acceptable longer response time depending on the amount of data processed.  General guidelines dictate that the response time should average between 2 - 3 seconds.  However, this period can be slightly extended by engaging the user during processing time by displaying appropriate notifications or messages.
