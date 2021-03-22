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
This script checks the weekly rewards for users.

USAGE:
To check at the beggining of the week that the rewards were updated properly.

"""

# My imports #
from surveys.models import User, Reward #type: ignore

# Grab students and rewards
totalStudents = User.objects.filter(studyID = 2).count()

# Grab students with 0 rewards
zeroWeeklyRewards = Reward.objects.filter(userID__studyID = 2, weeklyResponses = 0).count()
oneWeeklyReward = Reward.objects.filter(userID__studyID = 2, weeklyResponses = 1).count()
twoWeeklyRewards = Reward.objects.filter(userID__studyID = 2, weeklyResponses = 2).count()

#Print
print("\nTotal students for studyId 1: %d" % totalStudents)
print("Students with 0 Weekly Rewards: %d" % zeroWeeklyRewards)
print("Students with 1 Weekly Rewards: %d" % oneWeeklyReward)
print("Students with 2 Weekly Rewards: %d" % twoWeeklyRewards)
