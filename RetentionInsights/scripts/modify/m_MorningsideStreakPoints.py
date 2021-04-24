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
This script defautls adds streakPoints to Morningside students.

USAGE:
Made because the steakPoints were zeroed by accident on Week 6. (Week of Apr 19).
Note, max streak points a student could've had PRIOR to this week was 5.

"""

# My imports #
from surveys.models import User, Reward #type: ignore

# Grab students from Morningside Study
students = User.objects.filter(studyID = 2)

#Count students edited
count = 0

for student in students:
    #Get the student's reward
    rewards = Reward.objects.get(pk = student.userID)

    # Check if their current streak is ONE - means they answered at least this weeks' surveys
    #   if they hadn't, their streak would've zeroed either way.
    if (rewards.streakPoints == 1):
        count += 1

        print ("\n\nBEFORE CHANGE: Student %s -> %d" % (student.firstName, rewards.streakPoints))

        #Get the streak they possibly had before
        #? That is the floor() of the total responses minus 1.
        lostStreak = int(rewards.totalResponses / 2) - 1

        #Update their streakPoints
        rewards.streakPoints += lostStreak

        rewards.save()

        print ("\n\nAFTER CHANGE: Student %s -> %d" % (student.firstName, rewards.streakPoints))

#Final print
print ("\n\nUpdated %d student streaks" % count)

