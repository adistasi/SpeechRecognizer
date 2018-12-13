import nltk, pickle, csv, math, random
import MLUtils as utl
from nltk.classify import MaxentClassifier

'''
A method to open a CSV file and read in data, and split it into three dictionaries - one for training, one for development, and one for testing
'''


def CSV_To_Dictionary(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')  # make a reader to read though the rows

        # Create the lists for each type of classification
        english = []
        french = []
        german = []
        italian = []
        spanish = []

        # loop though the data in the CSV and add each question to it's corresponding list
        for question, tag in reader:
            if (tag == "en-GB"):
                english.append(question)
            elif (tag == "fr-FR"):
                french.append(question)
            elif (tag == "de-DE"):
                german.append(question)
            elif (tag == "it-IT"):
                italian.append(question)
            elif (tag == "es-DO"):
                spanish.append(question)

    f.close()

    # Actually split the data from 1 list into the train/dev/test lists
    enTrain, enTest = split_data(english)
    frTrain, frTest = split_data(french)
    grTrain, grTest = split_data(german)
    itTrain, itTest = split_data(italian)
    spTrain, spTest = split_data(spanish)


    # Format the data as a dictionary - not the most efficient way of doing it, but it quickly allowed me to reformat this as 3 dictionaries
    trainingData = {
        'en-GB': enTrain,
        'fr-FR': frTrain,
        'de-DE': grTrain,
        'it-IT': itTrain,
        'es-DO': spTrain
    }

    # These are only tagged to evaluate accuracy and to keep the data in a format acceptable by the classifier.
    # The tags are at NEVER shown to the classifiers and are only used to evaluate accuracy at the end
    # If I had a bigger dataset, this information would be held out entirely and tested separately
    testData = {
        'en-GB': enTest,
        'fr-FR': frTest,
        'de-DE': grTest,
        'it-IT': itTest,
        'es-DO': spTest
    }

    return trainingData, testData


'''
A method to randomly split a given list of data into 2 lists - a training list and a testing list
'''
def split_data(questionList):
    # Perform the necessary mathematical calculations to perform a 90%/10% split
    length = len(questionList)
    endTrain = int(math.floor(0.9 * length))

    random.shuffle(questionList)  # shuffle the data to ensure a random training set

    # Split and return the data into three lists
    return questionList[:endTrain], questionList[endTrain:]


if __name__ == "__main__":
    # split the data into two lists
    train, test = CSV_To_Dictionary('Datasets/TrainingData.csv')

    # result list instantiation and a definition of possible classes
    labeledTrain = []
    labeledTest = []
    possibleClassifications = ['en-GB', 'fr-FR', 'de-DE', 'it-IT', 'es-DO']

    print("----------EXTRACTING FEATURES----------")
    print("TRAINING SET")
    # Extract features (and print progress updates) for the training set
    for classification, transcriptions in train.items():
        print("\t" + classification)
        for position, transcription in enumerate(transcriptions):
            print("\t\t" + str(position + 1) + " of " + str(len(transcriptions)))
            labeledTrain.append((utl.get_features(transcription), classification))

    print("TEST SET (for accuracy purposes)")
    # Extract features and print progress updates for the test set (used for evaluation purposes, it is not involved with the training in any way)
    for classification, transcriptions in test.items():
        print("\t" + classification)
        for position, transcription in enumerate(transcriptions):
            print("\t\t" + str(position + 1) + " of " + str(len(transcriptions)))
            labeledTest.append((utl.get_features(transcription), classification))

    # Train the classifiers on the feature exctracted/labeled training set
    print("\n\n----------TRAINING CLASSIFIERS----------")
    print("\tTraining maxent")
    maxent = MaxentClassifier.train(labeledTrain)
    print("\tTraining Naive Bayes")
    nb = nltk.NaiveBayesClassifier.train(labeledTrain)
    print("\tTraining Decision Tree")
    dt = nltk.DecisionTreeClassifier.train(labeledTrain)

    # Implement the three classifiers into a Majority Votes Classifier
    classifier = utl.MajorityVotesClassifier([maxent, nb, dt])

    print("\n\n----------EVALUTATING CLASSIFIERS----------")
    print("-----OVERALL CLASSIFIER-----")
    # Evaluate each of the classifiers (The main Majority Votes and each individual classifier), printing out the accuracy & a confusion matrix for each
    errorCases = utl.EvaluateClassifier(classifier, labeledTest, test, possibleClassifications)

    print("-----MAXIMUM ENTROPY-----")
    maxentError = utl.EvaluateClassifier(maxent, labeledTest, test, possibleClassifications)

    print("-----NAIVE BAYES-----")
    nbError = utl.EvaluateClassifier(nb, labeledTest, test, possibleClassifications)

    print("-----DECISION TREE-----")
    dt = utl.EvaluateClassifier(dt, labeledTest, test, possibleClassifications)

    # Save it to disk, to allow for later use as a classifier
    outfile = open('languageClassifier.pickle', 'wb')
    pickle.dump(classifier, outfile)
    print("\nClassifier saved!");
    outfile.close()