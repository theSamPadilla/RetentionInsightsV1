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
This script adds users and rewards to a given study based on an excel sheet.

USAGE:
To add new users.
Remember to Add rewards!

"""

# My imports #
import pandas as pd
from surveys.models import Question_Text, Factor, User, Reward #type: ignore

# Check if study already has users
#!Keep this warning updated.
factors = User.objects.filter(studyID = 3).count()
if factors > 0:
    print ("WARNING: This study already has factors.\n",
        "\tIf you want to proceed, remove this warning in the code.")
    exit()

# Grab list of questions from file
filename = "SiouxRubber_EmployeeList.xlsx"
df = pd.read_excel(filename)

# Grab starting ID (highest questionTextID + 1) 
startingID = Question_Text.objects.last().questionTextID + 1

# Make list of objects
#!?Note that this defaults all the questions to Sliders
questions = [
    (Question_Text(startingID+index, row.FactorID,
        row.Question_Text, row.Positive_p,'S6'))
    for index, row in df.iterrows()
]

print ("Creating List of Questions from file", filename)

# Save each object
for q in questions:
    q.save()

print ("\nSaved %d new questions." % len(questions))
