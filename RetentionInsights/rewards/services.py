import os

from django.utils import timezone # type: ignore
from datetime import date
import pandas as pd #type: ignore
from django.core.mail import EmailMessage

from surveys.models import User, Reward, Study #type: ignore

class RewardService(object):
##############
# ATTRIBUTES #
##############
    # Define study path #
    studyIDToReportFolder = {
        1 : "test/",
        2 : "Morningside_Pilot/",
        3 : "Sioux_Rubber_Pilot/",
        4 : "Warehouse_Pilot/",
        5 : "State_Steel_Pilot/"
    }

    # Define Reward Dir
    rewardDir = "/home/sam/RetentionInsightsV1/reports/rewards/"

############################
# CHECK AND UPDATE Methods #
############################
    @classmethod
    def CheckRewardsForStudyID(cls, studyID):
        #Get all the users with the StudyID
        users = User.objects.filter(studyID = studyID)

        #Grab the stuyd object
        study = Study.objects.get(pk = studyID)

        #Make new report directory
        reportFolder = cls.rewardDir + cls.studyIDToReportFolder[studyID] + "Week " + str(study.week) + "/"
        os.mkdir(reportFolder)

        #Initialize response dictionary
        usersWithReward = {}

        #Reward Cases
        #!Two surveys per week - Reward ulocked weekly: Morningside, Test
        if studyID in (1, 2):
            #Define completed dic
            completed = {}
            
            #Get each user with 2 weekly responses
            for i in range(0, len(users)):
                user = users[i]
                userRewards = Reward.objects.get(userID = user.userID)

                if userRewards.weeklyResponses == 2:
                    usersWithReward[i] = [user.firstName, user.email, user.userGroup]
                    completed[i] = [user.firstName, user.email, user.userGroup]

            #Build extra report for completed
            RewardService.BuildReport(completed, users.count(), reportFolder, "week-completion-")

        #!Two surveys per week - Reward every month (8 responses): Sioux RUbber
        elif studyID == 3:
            #Define completed dic
            completed = {}

            #Check users who completed the survey this week AND those who got a reward
            for i in range(0, len(users)):
                user = users[i]
                userRewards = Reward.objects.get(userID = user.userID)

                #Reward unlocked
                if userRewards.streakPoints == 8:
                    usersWithReward[i] = [user.firstName, user.email, user.userGroup]

                #Surveys completed
                if userRewards.weeklyResponses == 2:
                    completed[i] = [user.firstName, user.email, user.userGroup]

            #Build extra report for completed
            RewardService.BuildReport(completed, users.count(), reportFolder, "week-completion-")

        #!One survey per week - Reward every 2 weeks: Tegra Warehouse
        elif studyID == 4:
            #Define completed dic
            completed = {}

            #Check users who completed the survey this week AND those who got a reward
            for i in range(0, len(users)):
                user = users[i]
                userRewards = Reward.objects.get(userID = user.userID)

                #Reward unlocked
                if userRewards.streakPoints == 2:
                    usersWithReward[i] = [user.firstName, user.email, user.userGroup]

                #Surveys completed
                if userRewards.weeklyResponses == 1:
                    completed[i] = [user.firstName, user.email, user.userGroup]

            #Build extra report for completed
            RewardService.BuildReport(completed, users.count(), reportFolder, "week-completion-")

        #!One survey per week - Reward every 4 cumulative responses: State Steel
        elif studyID == 5:
            #Define completed dic
            completed = {}

            #Check users who completed the survey this week AND those who got a reward
            for i in range(0, len(users)):
                user = users[i]
                userRewards = Reward.objects.get(userID = user.userID)

                #Reward unlocked
                if userRewards.totalResponses != 0 and userRewards.totalResponses % 4 == 0:
                    usersWithReward[i] = [user.firstName, user.email, user.userGroup]

                #Surveys completed
                if userRewards.weeklyResponses == 1:
                    completed[i] = [user.firstName, user.email, user.userGroup]

            #Build extra report for completed
            RewardService.BuildReport(completed, users.count(), reportFolder, "week-completion-")

        #Build report for unlocked reward
        RewardService.BuildReport(usersWithReward, None, reportFolder, "reward-unlocked-")

    @staticmethod
    def UpdateRewardsForStudyID(studyID):
        #Get all the users for this studyID
        users = User.objects.filter(studyID = studyID)

        #Iterate through the users and update rewards
        #!Morningside Rules
        if studyID == 2:
            for user in users:
                userRewards = Reward.objects.get(userID = user.userID)
                
                #Zero streak points.
                #? If the user didn't answer ANY surveys this week, he loses his streak
                if userRewards.weeklyResponses == 0:
                    userRewards.streakPoints = 0
                
                #Zero weekly rewards
                userRewards.weeklyResponses = 0

                #Save changes
                userRewards.save()
        
        #!Sioux Rubber and Test
        elif studyID in (1, 3):
            for user in users:
                userRewards = Reward.objects.get(userID = user.userID)
                
                #Zero streak points.
                #? If the user didn't answer ALL surveys this week, he loses his streak
                if userRewards.weeklyResponses != 2:
                    userRewards.streakPoints = 0
                
                #? The user got his reward this week (8 responses). Restart count
                if userRewards.streakPoints == 8:
                    userRewards.streakPoints = 0

                #Zero weekly rewards
                userRewards.weeklyResponses = 0

                #Save changes
                userRewards.save()

        #!Warehouse
        elif studyID == 4:
            for user in users:
                userRewards = Reward.objects.get(userID = user.userID)
                
                #Zero streak points.
                #? If the user didn't answer THE survey this week, he loses his streak
                if userRewards.weeklyResponses != 1:
                    userRewards.streakPoints = 0
                
                #? The user got his reward this week (2 responses). Restart count
                if userRewards.streakPoints == 2:
                    userRewards.streakPoints = 0

                #Zero weekly rewards
                userRewards.weeklyResponses = 0

                #Save changes
                userRewards.save()

        #!State Steel
        elif studyID == 5:
            for user in users:
                userRewards = Reward.objects.get(userID = user.userID)

                #Zero streak points.
                #? If the user didn't answer THE survey this week, he loses his streak
                #? Notice this has nothing to do with the reward. The reward for State Steel is
                #?  only based on total responses
                if userRewards.weeklyResponses != 1:
                    userRewards.streakPoints = 0

                #Zero weekly rewards
                userRewards.weeklyResponses = 0

                #Save changes
                userRewards.save()

        #Update study week
        study = Study.objects.get(pk = studyID)
        study.week += 1
        study.save()

        return True

###############
# LOG Methods #
###############
    # Log Requests to both Check and Update endpoints
    @staticmethod
    def LogRequest(request, verified, endpoint, status, error, studyID):
        #Get Client IP
        ip = RewardService.get_client_ip(request)

        #Get appropriate filename
        if endpoint == 'Check':
            filename = "/home/sam/RetentionInsightsV1/logs/rewards/CheckRewardsLog.txt"
        else:
            filename = "/home/sam/RetentionInsightsV1/logs/rewards/UpdateRewardsLog.txt"
        
        #Open file and get current time
        f = open(filename, "a")
        now = timezone.localtime(timezone.now()).strftime("%A, %b-%d-%Y at %H:%M:%S")

        #Write log and close file
        if error != None:
            f.write("\n%s token from IP %s on %s | Status: %s | StudyID: %d\r\nError: %s\n" %
            (verified, ip, now, status, studyID, error))
        else:
            f.write("\n%s token from IP %s on %s | Status: %s | StudyID: %d\r\n" %
            (verified, ip, now, status, studyID))
        
        f.close()

###############
# GET Methods #
###############
    @staticmethod
    def get_client_ip(request):
        #? Found this script online, so I am unsure of its full workings
        remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        
        # set the default value of the ip to be the REMOTE_ADDR if available
        ip = remote_address

        # try to get the first non-proxy ip (not a private ip) from the HTTP_X_FORWARDED_FOR
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            proxies = x_forwarded_for.split(',')
            
            # remove the private ips from the beginning
            while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)): #type: ignore
                proxies.pop(0)
                # take the first ip which is not a private one (of a proxy)
                if len(proxies) > 0:
                    ip = proxies[0]
                print ("IP Address",ip)
        
        return ip

#################
# OTHER Methods #
#################
    @staticmethod
    def BuildReport(rewardDic, totalParticipants, reportFolder, reportName):
        #Make pandas df
        df = pd.DataFrame.from_dict(rewardDic, orient='index', columns=['Name', 'Email', 'Position'])

        #Sort alphabetically and reset indexes
        df.sort_values(by='Name', inplace=True)
        df.reset_index(drop=True, inplace=True)

        #Check if all users completed the surveys (only relevant for completion reports)
        if totalParticipants == len(rewardDic):
            df = df.append({"Name": "All participants completed their surveys this week", "Email":"", "Position":""}, ignore_index=True)

        #Readjust indexes
        df.index += 1
        
        #Export to Excel file to appropriate Folder
        filename = reportFolder + reportName + str(date.today()) + ".xlsx"
        df.to_excel(filename)

    @classmethod
    def EamailReport(cls, studyID):
        #Grab study
        study = Study.objects.get(pk = studyID)

        #Define email contents
        subject = "Week " + str(study.week) + " Completion Reports"
        greeting = "Hey " + study.contactPerson + ",\n\nHope this email finds you well and having a great day so far."
        center = "\n\nThis is an automated email containing the completion reports for week " + str(study.week) + " of the study."
        footer = "\n\nFeel free to reply to this email if you have any questions.\n\n--\nThe Retention Insights Team."
        message = greeting + center + footer
        
        #Sender and receiver
        sender = "padilla.samuelk@gmail.com"
        receiver = [study.contactEmail]
        
        #Make email oject
        email = EmailMessage(
            subject = subject,
            body = message,
            from_email = sender,
            to = receiver
        )

        #Get the file paths
        reportFolder = cls.studyIDToReportFolder[studyID] + "Week " + str(study.week) + "/"
        path = cls.rewardDir + reportFolder
        completion = path + "week-completion-" + str(date.today()) + ".xlsx"
        reward = path + "reward-unlocked-" + str(date.today()) + ".xlsx"

        #Attach
        email.attach_file(completion)
        email.attach_file(reward)
        
        #Send
        email.send(fail_silently=False)