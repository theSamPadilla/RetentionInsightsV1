# pylint: disable=relative-beyond-top-level
# Django imports
from django.shortcuts import render, get_object_or_404 # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from django.views.decorators.http import require_GET, require_POST #type: ignore
from django.utils import timezone # type: ignore
from django.urls import reverse  # type: ignore
from django.views.decorators.cache import never_cache # type: ignore

# My imports
from .services import SurveyService
from .models import Survey, Question, Response, Reward, Question_Text, User

###############################
# Initiate the service object #
###############################
surveyService = SurveyService()

###############################
# GET #
###############################
#Don't allow cache to avoid resubmission on back button
@require_GET
@never_cache
def GetSurvey(request, token):
    #Validate the Survey exsts or raise 404
    survey = get_object_or_404(Survey, token=token)

    #Ensure survey has not been completed
    if (surveyService.IsSurveyCompleted(survey.surveyID)):
        return render(request, 'surveys/completed.html', {'user' : survey.userID, 'survey' : survey} )

    #Check if survey has Expired
    if (surveyService.IsSurveyExpired(survey.surveyID)):
        return render(request, 'surveys/expired.html', {'user' : survey.userID, 'expirationDate' : survey.expirationDate})

    #Get survey context from service
    context = surveyService.GetSurveyContext(survey)

    return render(request, 'surveys/index.html', context)

@require_GET
def GetRecordedView(request, token):
    survey = surveyService.GetSurveyFromToken(token)

    #Verify if Survey has not been responded (Only possible if a direct GET to this URL)
    if (not surveyService.IsSurveyCompleted(survey.surveyID)):
        #If not completed, redirect to survey page.
        return HttpResponseRedirect(reverse('surveys:GetSurvey', args=[token]))

    #Get Recorded Context
    context = surveyService.GetRecordedPageContextFromToken(token)
    
    return render(request, 'surveys/recorded.html', context)

###############################
# POST #
###############################
@require_POST
def SubmitResponse(request, token):
    #Get surveyID to avoid passing the survey object around
    surveyID = surveyService.GetSurveyIDFromToken(token)
    
    #Check if survey has been responded already (only possible on back button resubmission)
    if (surveyService.IsSurveyCompleted(surveyID)):
        return HttpResponseRedirect(reverse('surveys:GetSurvey', args=[token]))

    #Pop the crsf token from answers and pass them to service for processing
    answers = dict(request.POST.items())
    answers.pop('csrfmiddlewaretoken')

    # Create response objects and catch error
    if (not surveyService.CreateResponses(answers)):
        error = "Invalid Data Submitted"
        return render(request, 'surveys/error.html', {'error': error})
    
    # Mark Survey as Completed
    surveyService.UpdateSurvey(surveyID)

    # Update Rewards
    userID = surveyService.GetUserIDFromSurveyID(surveyID)
    surveyService.UpdateRewardsForUserID(userID)

    #Redirect to new veiw
    return HttpResponseRedirect(reverse('surveys:ResponseRecorded', args=[token]))