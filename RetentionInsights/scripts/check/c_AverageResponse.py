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
This script checks the average response for a studyID considering negative responses.

USAGE:
To check toda's survey.

"""

# My imports #
from surveys.models import Response #type: ignore

#! Update StudyID here - current: Sioux Rubber (ID = 3)
STUDY_ID = 5

# Grab all responses for the study ID
responses = Response.objects.filter(questionID__surveyID__userID__studyID = STUDY_ID)

# Grab all positive and negative responses
positive = responses.filter(questionID__questionTextID__positive_p = True).values_list("response", flat=True    )
negative = responses.filter(questionID__questionTextID__positive_p = False).values_list("response", flat=True)

# Transform all elements to ints
positiveInts = list(map(int, positive))
negativeInts = list(map(lambda x: 6 - int(x), negative))

# Sum positive and negative responses
positiveSum = sum(positiveInts)
negativeSum = sum(negativeInts)

# Calculate average
avg = format(((positiveSum + negativeSum) / len(responses)), '.2f')

print ("\nFor Study ID %d the average response was %s" % (STUDY_ID, avg))
print ("Positive Responses: %d" % len(positive))
print ("Negaive Responses: %d" % len(negative))
print ("Total Responses: %d" % len(responses))
