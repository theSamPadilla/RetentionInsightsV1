from django import template

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
def isPlural(responses):
    if responses > 1:
        return "responses"
    else:
        return "response"

# Registration #
register.filter('sub', substract)
register.filter('range', loopRange)
register.filter('plural', isPlural)
register.filter('subR_L', substract_right_to_left)
register.filter('mod', modulo)
