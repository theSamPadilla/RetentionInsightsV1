from django.utils import timezone # type: ignore
from datetime import date
import pandas as pd #type: ignore

from surveys.models import User, Reward, Study #type: ignore

class RewardService(object):
    
    # Valid only for Morningside College Reward Rules #
    @staticmethod
    def CheckRewardsForStudyID(studyID):
        #Get all the users with the StudyID
        users = User.objects.filter(studyID = studyID)

        #Initialize response dictionary
        usersWithReward = {}

        #Get each user with 2 weekly responses
        for user in users:
            userRewards = Reward.objects.get(userID = user.userID)

            if userRewards.weeklyResponses == 2:
                usersWithReward[user.firstName] = user.email

        #Make pandas df
        df = pd.DataFrame.from_dict(usersWithReward, orient='index', columns=['Name', 'Email'])

        #Export to Excel file to Morningside Folder
        path = "/home/sam/RetentionInsightsV1/RetentionInsights/rewards/reward_reports/Morningside_College/"
        filename = path + str(date.today()) + ".xlsx"
        df.to_excel(filename)

        return True

    # Valid only for Morningside College Reward Rules #
    @staticmethod
    def UpdateRewardsForStudyID(studyID):
        #Get all the users for this studyID
        users = User.objects.filter(studyID = studyID)

        #Iterate through the users and update rewards
        for user in users:
            userRewards = Reward.objects.get(userID = user.userID)
            
            #Zero streak points.
            #? If the user didn't answer any surveys this week, he loses his streak
            if userRewards.weeklyResponses == 0:
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
    def LogRequest(request, verified, endpoint, status):
        #Get Client IP
        ip = RewardService.get_client_ip(request)

        #Get appropriate filename
        if endpoint == 'Check':
            filename = "/home/sam/RetentionInsightsV1/RetentionInsights/rewards/logs/CheckRewardsLog.txt"
        else:
            filename = "/home/sam/RetentionInsightsV1/RetentionInsights/rewards/logs/UpdateRewardsLog.txt"
        
        #Open file and get current time
        f = open(filename, "a")
        now = timezone.localtime(timezone.now()).strftime("%A, %b-%d-%Y at %H:%M:%S")

        #Write log and close file
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