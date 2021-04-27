from django.db import models
from django.utils import timezone

class Study(models.Model):
    studyID = models.IntegerField(primary_key=True)
    studyName = models.CharField(max_length=200)
    organizationName = models.CharField(max_length=200)
    contactPerson = models.CharField(max_length=200)
    contactEmail = models.EmailField()
    feedbackUrl = models.CharField(max_length=200, unique=True)
    
    #Display funtions
    def data_points(self):
        return str(Response.objects.filter(questionID__surveyID__userID__studyID = self.studyID).count())

    def responses(self):
        return Survey.objects.filter(userID__studyID = self.studyID, completed_p = True).count()
    
    def active_participants(self):
        return str(User.objects.filter(studyID = self.studyID, active_p = True).count())

    def surveys_sent(self):
        return str(Survey.objects.filter(userID__studyID = self.studyID).count())

    def __str__(self):
        return self.studyName

class User(models.Model):
    userID = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    userGroup = models.CharField(max_length=200)
    studyID = models.ForeignKey(Study, on_delete=models.CASCADE)
    active_p = models.BooleanField(default=False)
    removed_p = models.BooleanField(default=False)
    age = models.IntegerField(default=None, blank=True, null=True)
    birthDate = models.DateField(default=None, blank=True, null=True)
    employmentTime = models.DurationField(default=None, blank=True, null=True)
    hireDate = models.DateField(default=None, blank=True, null=True)

    #Display name
    def total_responses(self):
        return str(Reward.objects.get(pk = self.userID).totalResponses)

    def __str__(self):
        return 'User ' + str(self.userID) + " (" + str(self.firstName) + ")"

class Factor(models.Model):
    factorID = models.IntegerField(primary_key=True)
    factorName = models.CharField(max_length=200)
    studyID = models.ForeignKey(Study, on_delete=models.CASCADE)
    description = models.TextField()
    
    #Display name
    def __str__(self):
        return self.factorName

class Survey(models.Model):
    surveyID = models.IntegerField(primary_key=True)
    token = models.CharField(max_length=20, unique=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(default=timezone.now)
    expirationDate = models.DateTimeField(null=True)
    completed_p = models.BooleanField(default=False)
    completionDate = models.DateTimeField(null=True, blank=True, default=None)
    
    #Displays
    def expired(self):
        now = timezone.localtime(timezone.now())
        return (now > self.expirationDate)
    expired.boolean = True

    def study(self):
        return self.userID.studyID

    def __str__(self):
        return ("Survey " + str(self.surveyID) + " for " +
        str(timezone.localtime(self.creationDate).strftime("%A, %b-%d-%Y at %H:%M:%S")) + 
        " | Token: " + str(self.token))

    def displayCreationDate(self):
        return str(timezone.localtime(self.creationDate).strftime("%A, %B %-d, %Y"))

    def displayCompletionDate(self):
        return str(timezone.localtime(self.completionDate).strftime("%A, %B %-d, %Y at %-I:%M %p"))

    def displayExpirationDate(self):
        return str(timezone.localtime(self.expirationDate).strftime("%A, %B %-d, %Y at %-I:%M %p"))

    #Meta for latest
    class Meta ():
        get_latest_by = "creationDate"

class Question_Text(models.Model):
    questionTextID = models.IntegerField(primary_key=True)
    factorID = models.ForeignKey(Factor, on_delete=models.CASCADE)
    text = models.TextField()
    positive_p = models.BooleanField(default=True)
    QUESTIONS_TYPE = [
        ('S6', 'Slider 1 to 6'),
        ('Bool', 'Boolean'),
        ('ST', 'Short Text'),
        ('LT', 'Long Text'),
    ]
    type = models.CharField(max_length=20, choices=QUESTIONS_TYPE)
    
    #Display fucntions
    def study(self):
        return str(self.factorID.studyID)

    def factor(self):
        return self.factorID

    def __str__(self):
        return self.text

class Question(models.Model):
    questionID = models.IntegerField(primary_key=True)
    surveyID = models.ForeignKey(Survey, on_delete=models.CASCADE)
    questionTextID = models.ForeignKey(Question_Text, on_delete=models.CASCADE)
    
    #Display functions
    def study(self):
        return str(self.questionTextID.factorID.studyID)
    
    def factor(self):
        return str(self.questionTextID.factorID)

    def text(self):
        return self.questionTextID.text

    def survey(self):
        return str(self.surveyID.surveyID)

    def __str__(self):
        return "Question " + str(self.questionID)

class Response(models.Model):
    questionID = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    response = models.CharField(max_length=200)

    #Display functions
    def study(self):
        return str(self.questionID.surveyID.userID.studyID)
    
    def text(self):
        return str(self.questionID.questionTextID)

    def __str__(self):
        return "Response for " + str(self.questionID)

class Reward(models.Model):
    userID = models.OneToOneField(User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    streakPoints = models.IntegerField(default=0)
    weeklyResponses = models.IntegerField(default=0)
    totalResponses = models.IntegerField(default=0)

    #Display functions
    def name(self):
        return self.userID.firstName

    def study(self):
        return self.userID.studyID

    def __str__(self):
        return "Rewards for " + str(self.userID)
