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
This script checks which user correspons to which phone number

USAGE:
To check which users are getting the text messages bounced back.

"""

# My imports #
from surveys.models import User #type: ignore

# Define phone numbers
numbers = ["7122023173", "6069401288"]

# Loop through numbers and find users
for num in numbers:
    user = User.objects.get(phoneNumber = num)

    #Print
    print ({"User": user.firstName, "Study": user.studyID, 
            "active?": user.active_p, "removed?": user.removed_p})