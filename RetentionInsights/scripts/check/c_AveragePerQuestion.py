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
This script checks the average response for EACH QUESTION for a given
studyID and outputs the result to an excel sheet in the same folder.

USAGE:
To build the excel sheet above.

"""

# My imports #
import pandas as pd
from datetime import date
from surveys.models import Response, Question_Text #type: ignore

#! Update StudyID here - current: Sioux Rubber (ID = 3)
STUDY_ID = 3

# Grab all responses for the study ID
responses = Response.objects.filter(questionID__surveyID__userID__studyID = STUDY_ID)

# Initialize Question ID Dictionary
#?This is questionTextID -> [frequency, response sum] 
questionTextId_to_ResponseSum_And_Frequency = {}

# Grab all responses for each Question_Text
for response in responses:
    id = response.questionID.questionTextID.questionTextID

    #?If the questionTestID is not in the dictionary, create the instance
    if id not in questionTextId_to_ResponseSum_And_Frequency:
        questionTextId_to_ResponseSum_And_Frequency[id] = [1, int(response.response)]

    #?questionTextID exists in the dictionary, update the occurance and the response sum
    else:
        questionTextId_to_ResponseSum_And_Frequency[id][0] += 1
        questionTextId_to_ResponseSum_And_Frequency[id][1] += int(response.response)



# Create Final Dict
#? QuestionTextId -> [questionText, factorID, positive_P, average]
finalDict = {}

for questionId in questionTextId_to_ResponseSum_And_Frequency:
    questionTextObj = Question_Text.objects.get(pk = questionId)
    finalDict[questionId] = [
        questionTextObj.text,
        questionTextObj.factorID.factorName,
        questionTextObj.positive_p,
        questionTextId_to_ResponseSum_And_Frequency[questionId][1] / questionTextId_to_ResponseSum_And_Frequency[questionId][0]
    ]

# Create df
df = pd.DataFrame.from_dict(finalDict, orient='index', columns=['Question', 'Factor', 'Is Positive?', 'Average (1 - 6)'])
df.sort_values(by=['Factor'], inplace=True)

# Export df
path = './AvgResponsePerQuestion_ID' + str(STUDY_ID) + '_' + str(date.today()) + '.xlsx'
df.to_excel(path, index=False)

print ("\nExcel File for Study ID %d created. Check current Folder." % STUDY_ID)
