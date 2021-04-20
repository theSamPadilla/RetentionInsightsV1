from django.utils import timezone # type: ignore
from datetime import date
import pandas as pd #type: ignore

from surveys.models import User, Reward, Study #type: ignore

class RewardService(object):
##############
# ATTRIBUTES #
##############
    # Define study path #
    studyIDToReportFolder = {
        1 : "test/",
        2 : "Morningside_Pilot/",
        3 : "Sioux_Rubber_Pilot/"
    }

############################
# CHECK AND UPDATE Methods #
############################
    @classmethod
    def CheckRewardsForStudyID(cls, studyID):
        #Get all the users with the StudyID
        users = User.objects.filter(studyID = studyID)

        #Define studyPath
        reportFolder = cls.studyIDToReportFolder[studyID]

        #Initialize response dictionary
        usersWithReward = {}

        #Reward Cases
        #!Two surveys per week: Morningside, Sioux Rubber, Test
        if studyID in (1, 2, 3):
            #Get each user with 2 weekly responses
            for i in range(0, len(users)):
                user = users[i]
                userRewards = Reward.objects.get(userID = user.userID)

                if userRewards.weeklyResponses == 2:
                    usersWithReward[i] = [user.firstName, user.email, user.userGroup]
                
        #Make pandas df
        df = pd.DataFrame.from_dict(usersWithReward, orient='index', columns=['Name', 'Email', 'Position'])

        #Sort alphabetically and reset indexes
        df.sort_values(by='Name', inplace=True)
        df.reset_index(drop=True, inplace=True)

        #Check if all users completed the surveys
        if users.count() == len(usersWithReward):
            df = df.append({"Name": "All participants completed their surveys", "Email":"", "Position":""}, ignore_index=True)

        #Readjust indexes
        df.index += 1
        
        #Export to Excel file to appropriate Folder
        path = "/home/sam/RetentionInsightsV1/reports/rewards/" + reportFolder
        filename = path + str(date.today()) + ".xlsx"
        df.to_excel(filename)

        return True

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
                
                #Zero weekly rewards
                userRewards.weeklyResponses = 0

                #Save changes
                userRewards.save()

        return True

###############
# LOG Methods #
###############
    # Log Requests to both Check and Update endpoints
    @staticmethod
    def LogRequest(request, verified, endpoint, status, error):
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
            f.write("\n%s token from IP %s on %s | Status: %s\r\nError: %s\n" %
            (verified, ip, now, status, error))
        else:
            f.write("\n%s token from IP %s on %s | Status: %s\r\n" %
            (verified, ip, now, status))
        
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