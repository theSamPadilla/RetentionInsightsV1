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
This script defautls the weeklyResponses of every user with more than ONE
weeklyResponse back to ONE.

USAGE:
Made because two surveys were sent on the same day by accident (3/16/21).

"""

# My imports #
from surveys.models import User, Reward #type: ignore

# Grab students for Morningside Study
students = User.objects.filter(studyID = 2)

twoRewards = 0

for student in students:
    rewards = Reward.objects.get(pk = student.userID)

    # Check if they have more than 1 weeklyResponses
    if (rewards.weeklyResponses > 1):
        print ("\n\nBEFORE CHANGE: Student %s -> %d" % (student.firstName, rewards.weeklyResponses))

        #Make weekly responses 1 and save
        rewards.weeklyResponses = 1
        rewards.save()

        print ("AFTER CHANGE: Student %s -> %d" % (student.firstName, rewards.weeklyResponses))

        twoRewards += 1

print (twoRewards)