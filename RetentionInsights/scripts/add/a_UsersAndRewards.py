## SETUP TO RUN THE SCRIPT ##
import os, sys

from pandas.core.indexes import multi
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
Delete the excel sheet after using it.
Remember to Add rewards!
Keep warnings updated.

"""

# My imports #
import pandas as pd
import datetime
from surveys.models import User, Reward #type: ignore

# Helper Function #
def GetEmploymentTime(timestr):
    #Get the num and month
    spltDur = timestr.split()
    num = int(spltDur[0])
    duration = spltDur[1]

    #Define days multipler
    if duration in ("YR", "YRS"):
        multiplier = 365.25 
    else:
        multiplier = 30

    #Define time duration in days    
    days = datetime.timedelta(days=num*multiplier)
    
    return days


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

# Grab starting ID (highest userID + 1) 
startingID = User.objects.last().userID + 1

# Make list of objects
users = [(
    User(
        startingID+index,   #userID
        row.Name,           #firstName
        row.Phone,          #phoneNumber
        None,               #email
        row.Position,       #userGroup
        3,                  #studyID #!SiouxRubber = 3
        True,               #active_p
        False,              #removed_p
        row.Age,            #age
        GetEmploymentTime(row.EmploymentTime)
        ))
    for index, row in df.iterrows()
]

print ("Creating List of users from file", filename)

# Save each object and create rewards
for u in users:
    reward = Reward(u.userID)
    u.save()
    reward.save()

print ("\nSaved %d new users and rewards." % len(users))
