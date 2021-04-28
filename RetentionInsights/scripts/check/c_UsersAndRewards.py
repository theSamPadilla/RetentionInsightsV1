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
This script checks the number of active users, total users, rewards, and removed users

USAGE:
To check the above.

"""

# My imports #
from surveys.models import User, Reward, Survey #type: ignore

# Grab students and rewards
studyID = 1
totalStudents = User.objects.filter(studyID = studyID).count()

# Check all students have rewards
#for student in totalStudents:
 #   if not Reward.objects.filter(pk = student.userID).exists():
  #      print("FUCK, ONE NON MATCHING REWARD")
   #     break

rewards = Reward.objects.filter(userID__studyID = studyID).count()
activeStudents = User.objects.filter(studyID = studyID, active_p = True).count()
removedStudents = User.objects.filter(studyID = studyID, active_p = False, removed_p = True).count()
pendingStudents = User.objects.filter(studyID = studyID, active_p = False, removed_p = False).count()

#Print
print("\nTotal users: %d" % totalStudents)
print("Rewards: %d" % rewards)

print("\nActive: %d" % activeStudents)
print("Removed: %d" % removedStudents)
print("Pending: %d" % pendingStudents)