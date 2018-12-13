import MLUtils as utl

'''
A simple method to return the classification of a question given the text of the question
'''
def predictLanguage(inputTrans):
    # Load the classifier created and saved by CreateClassifier.py
    classifier = utl.ReadModel('langaugeClassifier.pickle')
    return classifier.classify({ inputTrans: True })  # the dictionary format is required for the classifier, but the 'True' has no bearing on the classification

    return "en-GB"