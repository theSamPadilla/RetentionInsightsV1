# pylint: disable=relative-beyond-top-level
# Django imports
from django.http.response import HttpResponse #type: ignore
from django.shortcuts import render, get_object_or_404 # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from django.views.decorators.http import require_GET, require_POST #type: ignore
from django.urls import reverse  # type: ignore
from django.views.decorators.cache import never_cache # type: ignore

# My imports
from .services import ConfirmationService
from surveys.services import SurveyService #type: ignore
from surveys.models import Survey #type: ignore

################################
# Initiate the service objects #
################################
confirmationService = ConfirmationService()
surveyService = SurveyService()

###############################
# GET #
###############################
@require_GET
@never_cache
def GetConfirmationPage(request, token):
    #Validate the confirmation Survey exsts or raise 404
    survey = get_object_or_404(Survey, token=token)

    #If survey is not a confirmation survey, redirect to surveys app
    if (not confirmationService.CheckSurveyIsConfirmationSurveyType(survey.surveyID)):
        return HttpResponseRedirect(reverse('surveys:GetSurvey', args=[token]))

    #Ensure confirmation survey has not been completed and user is not active
    if (surveyService.IsSurveyCompleted(survey.surveyID) and survey.userID.active_p):
        return render(request, 'confirmation/completed.html', {'user' : survey.userID, 'survey' : survey})

    #Check if confirmation survey has Expired
    if (surveyService.IsSurveyExpired(survey.surveyID)):
        return render(request, 'confirmation/expired.html', {'user' : survey.userID, 'survey' : survey})

    #Get the user from the survey token
    user = surveyService.GetUserFromSurveyToken(token)

    #Make context
    context = {'user' : user, 'survey' : survey,}

    return render(request, 'confirmation/confirm.html', context)

@require_GET
def GetConfirmationRecordedPage(request, token):
    #Get survey to verify if it has been completed
    survey = surveyService.GetSurveyFromToken(token)

    #Verify if Survey has not been responded (Only possible if a direct GET to this URL)
    if (not surveyService.IsSurveyCompleted(survey.surveyID)):
        #If not completed, redirect to survey page.
        return HttpResponseRedirect(reverse('confirmation:GetConfirmationPage', args=[token]))

    #Get user
    user = surveyService.GetUserFromSurveyToken(token)
    
    return render(request, 'confirmation/recorded.html', {'user' : user})

###############################
# POST #
###############################
@require_POST
def SubmitConfirmation(request, token):
    #Get surveyID to avoid passing the survey object around
    surveyID = surveyService.GetSurveyIDFromToken(token)

    #Get userID from surveyID
    userID = surveyService.GetUserIDFromSurveyID(surveyID)

    #Confirm user and mark survey as completed
    confirmationService.ActivateUser(userID)
    surveyService.UpdateSurvey(surveyID)
    
    #Redirect to new veiw
    return HttpResponseRedirect(reverse('confirmation:ConfirmationRecorded', args=[token]))