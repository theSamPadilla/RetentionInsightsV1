from django import template

# Initialize registrator #
register = template.Library()

#Substraction filter
def substract(leftHand, rightHand):
    return int(leftHand) - int(rightHand)

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