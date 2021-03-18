## SETUP TO RUN THE SCRIPT ##
import os, sys
path = '/home/sam/RetentionInsightsV1/RetentionInsights/'
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RetentionInsights.settings.production")

import django
django.setup()
#############################

"""

DESCRIPTION:
This script deletes all the survey objects that belong to the Test study.
studyID = 1.

USAGE:
Clean up the db and make the admin console less cluttered with useless data.

"""

# My imports #
from surveys.models import Survey, Question, Response #type: ignore

# Grab all surveys, questions, and responses for Test Study
#? Note: Double Underscore notation references an attribute of the foreign key 
# !IMPORTANT studyID = 1!
testSurveys = Survey.objects.filter(userID__studyID = 1)
testQuestions = Question.objects.filter(surveyID__userID__studyID = 1)
testResponses = Response.objects.filter(questionID__surveyID__userID__studyID = 1)

print ("Test Surveys: %d" % len(testSurveys))
print ("Test Questions: %d" % len(testQuestions))
print ("Test Responses: %d" % len(testResponses))

# Delete test surveys (cascades into questions and responses)
if (len(testSurveys) > 0):
    print ("\nDeleting test surveys...")
    testSurveys.delete()

    # Grab objecst again and Final print
    testSurveys = Survey.objects.filter(userID__studyID = 1)
    testQuestions = Question.objects.filter(surveyID__userID__studyID = 1)
    testResponses = Response.objects.filter(questionID__surveyID__userID__studyID = 1)
    print ("\nTest Surveys: %d" % len(testSurveys))
    print ("Test Questions: %d" % len(testQuestions))
    print ("Test Responses: %d" % len(testResponses))

else:
    print ("\nNo test surveys to delete")