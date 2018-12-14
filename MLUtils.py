import nltk, pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from nltk.tag import map_tag
import string

'''
A class to allow for a Majority Votes Classifier System
The result with the most votes is returned as the classifier's answer
'''
class MajorityVotesClassifier(nltk.classify.api.ClassifierI):
    def __init__(self, classifiers):
        super(MajorityVotesClassifier, self).__init__()
        self.__classifiers = classifiers

    def labels(self):
        return list()

    def classify(self, data):
        """
        Classifies the given data sample.
        """
        votes = []
        for classifier in self.__classifiers:
            vote = classifier.classify(data)
            votes.append(vote)
        # The predicted value is the one that has more votes
        return max(set(votes), key=votes.count)


'''
A method to allow for accessing of a saved model.  Used in classifyQuestions.py to offer classification
'''
def ReadModel(modelFilename):
    return pickle.load(open(modelFilename, 'rb'))


'''
A method to extract features from the text
'''
def get_features(text):
    words = []

    # Tokenize the question as a sentence and then tokenize the sentence into words
    sentences = nltk.sent_tokenize(text.translate(None, string.punctuation))
    for sentence in sentences:
        words = words + nltk.word_tokenize(sentence)

    # Normalize/cast all words to lowercase
    words = [i.lower() for i in words]

    # Obtain & format bigram combinations from the sentence
    bigrams = nltk.bigrams(words)
    bigrams = ["%s %s" % (i[0], i[1]) for i in bigrams]

    # Obtain & format trigram combinations from the sentence
    trigrams = nltk.trigrams(words)
    trigrams = ["%s %s %s" % (i[0], i[1], i[2]) for i in trigrams]


    # Calculate the average word length in the sentence
    wlSum = 0
    for word in words:
        wlSum = wlSum + len(word)

    averageWordLength = []
    if len(words) != 0:
        averageWordLength.append(wlSum/len(words))
    else:
        averageWordLength.append(0)



    # combine the length, bigrams, & trigrams
    features = bigrams + trigrams + averageWordLength

    # Return those features as a dictionary
    features = dict([(i, True) for i in features])
    return features


'''
A method to plot a confusion Matrix for a classifier
'''
def PlotConfusionMatrix( \
        confusionMatrix,
        classifier,
        title='Confusion matrix',
        cmap=plt.cm.Blues
):
    plt.imshow( \
        confusionMatrix,
        interpolation='nearest',
        cmap=cmap
    )

    # Feature creation/addition for the Confusion Matrix
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classifier.labels()))
    plt.xticks(tick_marks, classifier.labels(), rotation=45)
    plt.yticks(tick_marks, classifier.labels())
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


'''
A method to evaluate classifier's accuracy on a testSet and create a confusion matrix
'''
def EvaluateClassifier(classifier, testSet, testLabeledData, possibleClassifications):
    print("Classifier's accuracy values:")

    onTestSetAccuracy = nltk.classify.accuracy(classifier, testSet)

    print("\tOn test set = {}".format(onTestSetAccuracy))

    # List to store the cases where the algorithm made a mistake
    errorCases = []

    enCount = 0
    frCount = 0
    geCount = 0
    itCount = 0
    spCount = 0
    enRight = 0
    geRight = 0
    frRight = 0
    itRight = 0
    spRight = 0


    # plotting Confusion Matrix
    y_test, y_pred = [], []
    for (tag, transcriptions) in testLabeledData.items():
        # Find errors
        for transcription in transcriptions:
            guess = classifier.classify(get_features(transcription))

            if tag == "en-GB":
                enCount = enCount + 1
                if guess == tag:
                    enRight = enRight + 1
            elif tag == "fr-FR":
                frCount = frCount + 1
                if guess == tag:
                    frRight = frRight + 1
            elif tag == "de-DE":
                geCount = geCount + 1
                if guess == tag:
                    geRight = geRight + 1
            elif tag == "it-IT":
                itCount = itCount + 1
                if guess == tag:
                    itRight = itRight + 1
            elif tag == "es-DO":
                spCount = spCount + 1
                if guess == tag:
                    spRight = spRight + 1

            if guess is None or tag is None:  continue

            y_pred.append(possibleClassifications.index(guess))
            y_test.append(possibleClassifications.index(tag))

            if guess != tag:
                caseDescription = "question {0} prediction:{1}, real: {2}".format(transcription, guess, tag)
                errorCases.append(caseDescription)

    print("\n\t-----TAG ACCURACY-----")
    print("\t\tEnglish = " + str(enRight / enCount))
    print("\t\tFrench = " + str(frRight / frCount))
    print("\t\tGerman = " + str(geRight / geCount))
    print("\t\tItalian = " + str(itRight / itCount))
    print("\t\tSpanish = " + str(spRight / spCount))


    # Create the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)
    print('\n\nConfusion matrix, without normalization for the Classifier\n')
    print(cm)
    plt.figure()
    PlotConfusionMatrix(cm, classifier)

    return errorCases