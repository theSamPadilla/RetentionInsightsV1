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
This script checks the if the streakPoints has the proper limit. You have to define the
limit based on the week of the study

USAGE:
To check the above.

"""

# My imports #
from surveys.models import Reward #type: ignore

#!Enter studyID and limit here.
studyID = 2
limit = 6

# Grab students for study with more than reward limit
moreThanSix = Reward.objects.filter(userID__studyID = studyID, streakPoints__gt = limit)

if len(moreThanSix) > 0:
       print ("\nThese users in Study %d have more than %d streakPoints:" % (studyID, limit))
       
       for student in moreThanSix:
              print(student)

else:
   print("\nNo users in study %d have more than %d streak points" % (studyID, limit))