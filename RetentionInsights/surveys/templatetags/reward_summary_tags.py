from django import template
from datetime import timedelta
from ..models import Survey

# Initialize registrator #
register = template.Library()


#Substraction filter
def substract(leftHand, rightHand):
    return int(leftHand) - int(rightHand)

#Right to Left Substractin filter
def substract_right_to_left(leftHand, rightHand):
    return int(rightHand) - int(leftHand)

#Modulo filter
def modulo(leftHand, rightHand):
    print(leftHand)
    print(rightHand)
    print(int(leftHand) % int(rightHand))
    return int(leftHand) % int(rightHand)


#Loop filter
def loopRange (value):
    return range(0, value)

#Plural filter
def isPlural(responses, studyID):
    #Test
    if studyID == 1:
        if responses == 7:
            return "response"
        else:
            return "responses"

    #Morningside - Reward every WEEK for two responses
    if studyID == 2:
        if responses == 1:
            return "response"
        else:
            return "responses"

    #Sioux Rubber - Reward every MONTH for 8 responses
    elif studyID == 3:
        if responses == 7:
            return "response"
        else:
            return "responses"
    
    #Sioux Rubber - Reward every MONTH for 8 responses
    elif studyID == 4:
        if responses == 1:
            return "response"
        else:
            return "responses"
    
    #Sioux Rubber - Reward every 4 cumulative responses
    elif studyID == 5:
        if responses % 4 == 3:
            return "response"
        else:
            return "responses"

#How many study mates have completed the survey
def partenersCompleted(studyID, surveyID):
    #Get survey creation time
    created = Survey.objects.get(pk=surveyID).creationDate.date()
    oneDayLater = created + timedelta(hours=24)

    #Count all surveys with the studyID, created in the same day, and completed    
    return Survey.objects.filter(userID__studyID = studyID, creationDate__gt = created,
        creationDate__lt = oneDayLater, completed_p = True).count()

# Registration #
register.filter('sub', substract)
register.filter('subR_L', substract_right_to_left)
register.filter('mod', modulo)
register.filter('range', loopRange)
register.filter('plural', isPlural)
register.filter('completed', partenersCompleted)