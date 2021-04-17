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
This script checks the completed surveys and recorded responses for today.

USAGE:
To check toda's survey.

"""

# My imports #
from surveys.models import Survey, Response #type: ignore

# Grab all surveys for today
todaySurveys = Survey.objects.filter(creationDate__gte = '2021-01-13', userID__studyID = 2)

# Grab completed surveys
completed = todaySurveys.filter(completed_p = True)

# Grab all responses for today
responses = Response.objects.filter(questionID__surveyID__creationDate__gte = '2021-01-13',
            questionID__surveyID__completed_p = True, 
            questionID__surveyID__userID__studyID = 2)

print ("\nToday Surveys for Morningside College: %d" % len(todaySurveys))
print ("Completed Surveys today: %d" % len(completed))
print ("Recorded Responses today: %d" % len(responses))
