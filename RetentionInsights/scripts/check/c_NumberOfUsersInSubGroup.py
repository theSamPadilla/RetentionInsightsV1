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
This script checks how many users exist for a given subgroup for a given study.

USAGE:
To check the above.

"""

# My imports #
from surveys.models import User, Reward #type: ignore

# Define global vars #
STUDY_ID = 5
RESPONSE_THRESHOLD = 3

# Grab users for this study #
users = User.objects.filter(studyID = STUDY_ID)

# Define subgroup to filter through #
#! For now this is location.
location = {}

# Iterate over the users and count only those with more than 3 responses 
for user in users:
    
    #?Check if the user has more than 3 responses
    if Reward.objects.get(pk = user.userID).totalResponses > RESPONSE_THRESHOLD:
        
        #?If the user's location has already been seen, add one more locaiton
        if user.location in location:
            location[user.location] += 1
        #?Else add it to the dictionary
        else:
            location[user.location] = 1

#Print
print ("\nNumber of different subcategories: %d" % len(location))
print ("Total number of users above the %d response threshold: %d" %
(RESPONSE_THRESHOLD, sum(location.values())))
print("\nThe subcategory division is:", location)
