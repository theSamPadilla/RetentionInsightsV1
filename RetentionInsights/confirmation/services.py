from surveys.models import User, Question, Survey #type: ignore

class ConfirmationService(object):
####################
# CHECK Conditions #
####################
    @staticmethod
    def CheckSurveyIsConfirmationSurveyType(surveyID):
        #Get all the question objects with this surveyID
        questions = Question.objects.filter(surveyID = surveyID)

        #A confirmation survey has no question attached
        if (len(questions) != 0):
            return False

        return True

##################
# UPDATE Methods #
##################
    @staticmethod
    def ActivateUser(userID):
        #Get user
        user = User.objects.get(pk=userID)
        
        #Mark user as active
        user.active_p = True
        user.save()

        return True