# Python Imports #
from random import randint
from django.core.mail import send_mail

# My Imports #
from surveys.models import Study #type: ignore
from .models import Feedback

class FeedbackService(object):

###############
# GET Objects #
###############
    @staticmethod
    def GetFeedbackContext(study):
        return {
            "studyID" : study.studyID,
            "urlName" : study.feedbackUrl,
            "name" : study.organizationName,
            "person" : study.contactPerson
        }

    @staticmethod
    def GetRecordedContext(study):
        #Get random image
        img = "/feedback/img/img-" + str(randint(1, 6)) + ".jpg"
        
        return {
            "studyID" : study.studyID,
            "urlName" : study.feedbackUrl,
            "image" : img,
            "name" : study.organizationName,
            "person" : study.contactPerson,
            "email" : study.contactEmail
        }

##################
# CREATE Objects #
##################
    @staticmethod
    def CreateFeedback(data, name):
        #Get study
        study = Study.objects.get(feedbackUrl = name)

        #Get feedback text from data dictionary
        text = data["feedback"]

        #Create and save response
        newFeedback = Feedback(studyID = study, text = text)
        newFeedback.save()

        return newFeedback

#########
# OTHER #
#########
    @staticmethod
    def SendEmail(feedback):
        #Get study
        study = feedback.studyID

        #Define email contents
        subject = "[EMPLOYEE FEEDBACK] - Retention Insights"
        messageHeader = study.contactPerson + ", this is an automated email to notify you that on " + str(feedback.displayTimetamp()) + " an employee submitted the following anonymous feedback:\n\n\n\""
        messageFooter = "\"\n\n\nFeel free to reply to this email if you have any questions for us.\n- The Retention Insights Team."
        message = messageHeader + feedback.text + messageFooter
        
        #Sender and receiver
        sender = "padilla.samuelk@gmail.com"
        receiver = [study.contactEmail]

        #Send
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )