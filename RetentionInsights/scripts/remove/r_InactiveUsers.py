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
This script checks the number of active users for a given study and
removes all the inactive users (marks them as removed).

USAGE:
Made for to remove students who didn't confirm their participation for the
Morningside College Study.

"""

# My imports #
from surveys.models import User #type: ignore

# Grab students for Morningside Study
students = User.objects.filter(studyID = 2)
print ("\nTotal users in study: ", len(students))

# Grab active users
active = students.filter(active_p = True)
print ("\nActive users: ", len(active))

# Grab inactive users
inactive = students.filter(active_p = False)
print ("Inactive users: ", len(inactive))

# Grab pending students
pending = students.filter(active_p = False, removed_p = False)
print ("Pending users: ", len(pending))

# Grab removed users
removed = students.filter(removed_p = True)
print ("Removed users: ", len(removed))

# Mark users as removed
print ("\nRemoving Inactive...")
inactive.update(removed_p = True)

# Final print
print ("\nActive users: ", len(active))
removedANDinactive = students.filter(removed_p = True, active_p = False)
print ("Removed AND Inactive users: ", len(removedANDinactive))
pending = students.filter(active_p = False, removed_p = False)
print ("Pending users: ", len(pending))