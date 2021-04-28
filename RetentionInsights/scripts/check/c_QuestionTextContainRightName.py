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
This script checks whether some of the added questions contain the wrong name for the facility

USAGE:
To check the above.

"""

# My imports #
from surveys.models import Question_Text, Survey #type: ignore

# Grab active students
#!Big Soo Warehouse ID
questions = Question_Text.objects.filter(factorID__studyID = 4)

wrongName = 0

# Check how many surveys each has
for question in questions:
    #!Add the name of the previous study here
    if "Sioux Rubber" in question.text:
        wrongName += 1 

    print ("\nChecking %s" % question.text)


#Print
print ("\nChecked %d questions" % len(questions))
print ("\nQuestions with wrong name: %d" % wrongName)