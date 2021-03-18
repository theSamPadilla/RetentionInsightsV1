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
This script checks that the users have the appropriate number
of rewards for the surveys they completed.

USAGE:
Made because of two surveys were sent on the same day by accident.

"""

# My imports #
from surveys.models import User, Reward, Survey #type: ignore

# Grab students
students = User.objects.filter(studyID = 2)

twoRewards = 0

for student in students:
    rewards = Reward.objects.get(pk = student.userID)

    # Put the date below
    surveys = Survey.objects.filter(userID = student.userID, completed_p = True).filter(creationDate__gte = '2021-03-16')

    print ("\n\nStudent %s" % student.firstName)
    print ({len(surveys) : rewards.weeklyResponses})

    # you dont' want this if to get triggered #
    if (len(surveys) != rewards.weeklyResponses):
        print ("SOMETHING VERY BAD HAPPENED WITH REWARDS")
        break

    if (rewards.weeklyResponses == 2):
        twoRewards += 1

print (twoRewards)