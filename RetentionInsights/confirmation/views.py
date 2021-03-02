# pylint: disable=relative-beyond-top-level
# Django imports
from django.http.response import HttpResponse #type: ignore
from django.shortcuts import render, get_object_or_404 # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from django.views.decorators.http import require_GET, require_POST #type: ignore

# My imports
from .services import ConfirmationService

###############################
# Initiate the service object #
###############################
confirmationService = ConfirmationService()

###############################
# GET #
###############################
@require_GET
def GetConfirmationPage(request, token):
    #Get the user from the survey token
    user = confirmationService.GetUserFromSurveyToken(token)

    return render(request, 'confirmation/index.html', {'user':user})