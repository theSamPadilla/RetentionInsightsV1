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
This script adds the question_texts for each factor of a study.

USAGE:
This script builds the question_text object based on an excel sheet.
Add the excel sheet to the current folder and delete afterwards.
The excel sheet has 3 cols (factorId, question text, positive_p).
Each row represents a question.
Make sure to check the respective factorID for each factor in the admin portal when making
the spreadsheet.

"""

# My imports #
import pandas as pd
from surveys.models import Question_Text, Factor #type: ignore

# Check if study already has factors
#!Keep this warning updated.
factors = Factor.objects.filter(studyID = 3).count()
if factors > 0:
    print ("WARNING: This study already has factors.\n",
        "\tIf you want to proceed, remove this warning in the code.")
    exit()

# Grab list of questions from file
filename = "SiouxRubber_Questions.xlsx"
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
