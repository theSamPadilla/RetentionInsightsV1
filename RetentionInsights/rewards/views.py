# Django imports
from os import error
from django.http.response import HttpResponseRedirect #type: ignore
from django.http import HttpResponse #type: ignore
from django.shortcuts import render #type: ignore
from django.views.decorators.http import require_GET, require_POST #type: ignore
from django.urls import reverse #type: ignore
from django.conf import settings #type: ignore

# My imports
from .services import RewardService

###############################
# Initiate the service object #
###############################
rewardService = RewardService()
VERIFY_TOKEN = settings.REWARDS_VERIFY_TOKEN

###############################
# GET #
###############################
@require_GET
def CheckRewards (request, studyID, token):
    if token != VERIFY_TOKEN:
        #Log unverfied token
        rewardService.LogRequest(request, verified="UNVERIFIED", endpoint='Check', status="DENIED", error=None, studyID = studyID)
        return HttpResponse("Access denied.", content_type="text/plain")

    else:
        try:
            rewardService.CheckRewardsForStudyID(studyID)
        
        except Exception as e:
            #Log check error.
            rewardService.LogRequest(request, verified="Verified", endpoint='Check', status="ERROR", error=e, studyID = studyID)
            message = "An error occured: " + str(e) 
            return HttpResponse(message, content_type="text/plain")

        #Log succesful and verified check
        rewardService.LogRequest(request, verified="Verified", endpoint='Check', status="SUCCESSFUL", error=None, studyID = studyID)
        return HttpResponse("Report File Succesfully created.", content_type="text/plain")

@require_GET
def UpdateRewards (request, studyID, token):
    #Log unverfied token
    rewardService.LogRequest(request, verified="UNVERIFIED", endpoint='Update', status="DENIED", error=None, studyID = studyID)
    if token != VERIFY_TOKEN:
        return HttpResponse("Access denied.", content_type="text/plain")
    
    else:
        try:
            rewardService.UpdateRewardsForStudyID(studyID)

        except Exception as e:
            #Log failed update
            rewardService.LogRequest(request, verified="Verified", endpoint='Update', status="ERROR", error=e, studyID = studyID)
            message = "An error occured " + str(e) 
            return HttpResponse(message, content_type="text/plain")

        #Log succesful update
        rewardService.LogRequest(request, verified="Verified", endpoint='Update', status="SUCCESSFUL", error=None, studyID = studyID)
        message = "Rewards for study " + str(studyID) + " have been succesfully updated."
        return HttpResponse(message, content_type="text/plain")

###############################
# POST #
###############################