
from surveys.models import Survey #type: ignore

class ConfirmationService(object):

###############
# GET Methods #
###############
    @staticmethod
    def GetUserFromSurveyToken(token):
        survey = Survey.objects.get(token=token)
        return survey.userID
