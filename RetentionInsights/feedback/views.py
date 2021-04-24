from django.shortcuts import render, get_object_or_404 # type: ignore
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import never_cache
from django.urls import reverse

# My Imports #
from .services import FeedbackService
from surveys.models import Study #type: ignore

###############################
# Initiate the service object #
###############################
feedbackService = FeedbackService()

###############################
# GET #
###############################
#Don't allow cache to avoid resubmission on back button
@require_GET
@never_cache
def GetFeedbackPage(request, name):
    #Get the study by the unique url name
    study = get_object_or_404(Study, feedbackUrl = name)
    
    #Get context
    context = feedbackService.GetFeedbackContext(study)
    
    #Render 
    return render(request, 'feedback/index.html', context)

@require_GET
def GetRecordedPage(request, name):
    #Get the study by the unique url name
    study = get_object_or_404(Study, feedbackUrl = name)
    
    #Get context
    context = feedbackService.GetRecordedContext(study)
    
    #Render recorded page
    return render(request, 'feedback/recorded.html', context)

###############################
# POST #
###############################
@require_POST
def SubmitFeedback(request, name):
    #Pop the crsf token from answers and pass them to service for processing
    data = dict(request.POST.items())
    data.pop('csrfmiddlewaretoken')

    #Create feedback object
    newFeedback = feedbackService.CreateFeedback(data, name)

    #Send automated email to contact person
    feedbackService.SendEmail(newFeedback)
    
    #Redirect to new veiw
    return HttpResponseRedirect(reverse('feedback:FeedbackRecorded', args=[name]))