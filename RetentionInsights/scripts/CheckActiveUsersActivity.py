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
This script checks how many non confirmation surveys active users have answered

USAGE:
To check the above.

"""

# My imports #
from surveys.models import User, Reward, Survey #type: ignore

# Grab active students
activeStudents = User.objects.filter(studyID = 2, active_p = True, removed_p = False)

noResponses = 0
totalResponses = 0
inactiveStudents = []

# Check how many surveys each has
for student in activeStudents:
    rewards = Reward.objects.get(pk = student.userID)

    print ("\n\nStudent %s" % student.firstName)
    print ({'Total Respnses' : rewards.totalResponses})

    # check if the student has any total responses #
    if (rewards.totalResponses == 0):
        noResponses += 1
        inactiveStudents.append(student)

    else:
        totalResponses += rewards.totalResponses

#Print
print ("\nStudents with no responses yet: %d" % noResponses)
print("These students are:", inactiveStudents)
print ("\nAverage responses per active student: {:.2f}".format(float(totalResponses/len(activeStudents))))