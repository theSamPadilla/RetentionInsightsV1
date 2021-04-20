from django.utils import timezone # type: ignore
from datetime import timedelta
from random import randint

from .models import Survey, Question, Response, Reward, Question_Text, User

class SurveyService(object):
    
###############
# GET Objects #
###############
    @staticmethod
    def GetStudyIDFromSurveyID(surveyID):
        user = Survey.objects.get(pk = surveyID).userID
        return user.studyID.studyID
    
    @staticmethod
    def GetStudyIDFromUserID(userID):
        user = User.objects.get(pk = userID)
        return user.studyID.studyID
 
    @staticmethod
    def GetSurveyIDFromToken(token):
        survey = Survey.objects.get(token=token)
        return survey.surveyID

    @staticmethod
    def GetSurveyFromToken(token):
        return Survey.objects.get(token=token)

    @staticmethod
    def GetUserIDFromSurveyID(surveyID):
        survey = Survey.objects.get(pk=surveyID)
        return survey.userID.userID

    @staticmethod
    def GetSurveyQuestions(surveyID):
        return Question.objects.filter(surveyID = surveyID)

    @staticmethod
    def GetUserFromSurveyToken(token):
        survey = Survey.objects.get(token=token)
        return survey.userID

    @staticmethod
    def GetRewardsForUserID(userID):
        return Reward.objects.get(pk = userID)

    @staticmethod
    def GetSurveyContext(survey):
        #Get User and questions
        user = survey.userID
        rewards = SurveyService.GetRewardsForUserID(user.userID)
        questions = SurveyService.GetSurveyQuestions(survey.surveyID)

        #Return context
        return {
            'survey': survey,
            'user': user,
            'questions': questions,
            'rewards' : rewards,
        }

    @staticmethod
    def GetRecordedPageContextFromToken(token):
        user = SurveyService.GetUserFromSurveyToken(token)
        rewards = SurveyService.GetRewardsForUserID(user.userID)
        studyID = user.studyID.studyID
        image = None
        unlocked = False
        
        #Make week streak plural
        if rewards.streakPoints < 2:
            plural = "Point"

        #Verify if the user has unlocked the rewards
        #!Morningside or test - reward every 2 weekly responses
        if studyID == 2 or studyID == 1:
            if rewards.weeklyResponses == 2:
                image = "/surveys/img/morningside/img-" + str(randint(1, 14)) + ".jpg" 
                unlocked = True

        #!Sioux Rubber - reward every 8 monthly responses
        elif studyID == 3:
            #Reward ulocked
            if rewards.streakPoints == 8:
                image = "/surveys/img/sioux_rubber/reward/srb-mney-" + str(randint(1, 5)) + ".jpg" 
                unlocked = True

        return {
            'user' : user,
            'rewards' : rewards,
            'studyID' : studyID,
            'unlocked' : unlocked,
            'image' : image,
        }

####################
# CHECK Conditions #
####################
    # Check if the Survey has expired
    @staticmethod
    def IsSurveyExpired(surveyID):
        survey = Survey.objects.get(pk = surveyID)

        now = timezone.localtime(timezone.now())
        return (now > survey.expirationDate) #If now is greater, it has expired

    # Check if the Survey has been
    @staticmethod
    def IsSurveyCompleted(surveyID):
        survey = Survey.objects.get(pk = surveyID)

        return (survey.completed_p == True)     


###########################
# CREATE / UPDATE Objects #
###########################
    # Create Responses
    @staticmethod
    def CreateResponses(answers):
        #Create the response objects for each question
        #?The answers are a dic: 'questionID' -> 'response'
        for key, val in answers.items():
            #Get question object from id
            question = Question.objects.get(pk = int(key))

            #Check type for slider responses
            if (question.questionTextID.type == 'S6'):
                #This shouldn't ever happen
                if int(val) == 4:
                    return False
                #Answers greater than 4 (4 is null), must be one less
                elif int(val) > 4:
                    val = str(int(val) - 1)
                
            #Store and save new response object
            newResponse = Response(questionID = question, response = val)
            newResponse.save()

        return True

    # Update Survey
    @staticmethod
    def UpdateSurvey(surveyID):
        survey = Survey.objects.get(pk = surveyID)
        
        #Mark completionDate as now and mark as completed
        survey.completionDate = timezone.localtime(timezone.now())
        survey.completed_p = True
        survey.save()

    # Update Rewards
    @staticmethod
    def UpdateRewardsForUserID(userID):
        #?Note: The weekly rewards and streak points are getting checked and zeroed
        #? automatically at the start of the week
        #Update total responses
        rewards = Reward.objects.get(pk = userID)
        rewards.totalResponses += 1

        #Get Study ID
        studyID = SurveyService.GetStudyIDFromUserID(userID)
        
        #Update Streak Points for non Morningside users everytime
        if studyID != 2:
            rewards.streakPoints += 1
        
        #!Morningside only rule
        #? If the user's weeklyResponse is greater than 0, he already got
        #? the strak points for the week 
        elif rewards.weeklyResponses == 0:
            rewards.streakPoints += 1

        #Update Weekly rewards
        rewards.weeklyResponses += 1

        #Save rewards
        rewards.save()