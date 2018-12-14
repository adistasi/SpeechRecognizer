import MLUtils as utl

'''
A simple method to return the classification of a question given the text of the question
'''
def predictLanguage(inputTrans):
    # Load the classifier created and saved by CreateClassifier.py
    classifier = utl.ReadModel('languageClassifierThree.pickle')

    #Extract the features, feed it into the classifier, and return the result
    languageFeatures = utl.get_features(inputTrans)
    return classifier.classify(languageFeatures)
