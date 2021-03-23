import random , datetime , random , string , argparse , functools
import sqlite3
from twilio.rest import Client

BASE_URL = 'www.retentioninsights.io/confirmation/'

parser = argparse.ArgumentParser(description='Let us spawn some surveys.')
parser.add_argument('--studyid', type=int, help='Which study should we spawn surveys for?' , default=1 )
parser.add_argument('--duration', type=int , help='Number of days the survey is valid for.' , default=7 )
args = parser.parse_args()

def dt_to_django( dt_in ):
    return dt_in.strftime( '%Y-%m-%d %H:%M:%S' )
def dt_to_human( dt_in ):
    return dt_in.strftime( '%m/%d' )

def generate_token( existing_tokens ):
    while True:                # keep generating until a unique one is found
        token = functools.reduce( lambda x,y: x+y , random.choices( string.ascii_lowercase + string.digits , k=6 ) )
        if token not in existing_tokens:
            return token


# Account SID from twilio.com/console
account_sid = "AC6f01e296408ba99c27337463dd167164"
# Auth Token from twilio.com/console
auth_token  = 'e03305604429eea23d2c868c76149306'
twilio_client = Client(account_sid, auth_token)

conn = sqlite3.connect( '/home/sam/RetentionInsightsV1/RetentionInsights/db.sqlite3' )
c = conn.cursor()

#
# grab all existing tokens in the surveys table
#

result = c.execute( 'SELECT token FROM surveys_survey' )
existing_tokens = [ r[0] for r in result ]

#
# grab all users for the supplied study id
#

result = c.execute( 'SELECT * FROM surveys_user WHERE studyID_id=? AND active_p=false AND removed_p=false' , ( args.studyid , ) )
user_records = [ r for r in result ]

#
# for each user ...
#

for user in user_records:

    #
    # create a survey request record
    # * create the start / end date-times
    # * generate a unique token
    # * insert into DB
    # * !!!survey request must not be associated with any questions!!!
    #
    timezone = datetime.timezone( datetime.timedelta( hours=-5 ) )
    start_dt = datetime.datetime.now( timezone )
    end_dt = datetime.datetime.now( timezone ) + datetime.timedelta(days=args.duration)
    end_dt = end_dt.replace( hour = 23 , minute=59 , second=59 )

    token = generate_token( existing_tokens )
    existing_tokens += [token]

    result = c.execute( 'INSERT INTO surveys_survey (completed_p , userID_id , expirationDate , creationdate , token ) VALUES (False , ? , ? , ? , ?)' ,
                        ( user[0] ,
                          dt_to_django( end_dt ) ,
                          dt_to_django( start_dt ) ,
                          token ) )
    conn.commit()
    new_survey_id = c.lastrowid

    #
    # send SMS with survey request
    #

    try:
        message = twilio_client.messages.create(
            to='+1'+user[2] ,
            from_='+16072282179',
            # body='Howdy ' + user[1].strip() + '! This is a reminder to please verify your participation in the Morningside student well-being project by following the supplied link at http://'+BASE_URL+token+'. Please complete your confirmation on or before ' + dt_to_human( end_dt ) + '.  Free drinks!' )
            body='Hello ' + user[1].strip() + '!  Please verify your participation in the Morningside student well-being project by following the supplied link at http://'+BASE_URL+token+'. Please complete your confirmation on or before ' + dt_to_human( end_dt ) + '.  Free drinks!' )
        print( 'SMS sent to user' , user[0] , user[1] , 'at' , user[2] )
    except Exception as e:
        print( 'Recieved exception when sending survey request URL.' , e )
        print( 'Error when sending SMS sent to user' , user[0] , user[1] , 'at' , user[2] )

#
# ... end for each user
# 

conn.close()
