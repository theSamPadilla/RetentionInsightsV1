import random , datetime , random , string , argparse , functools
import sqlite3
from twilio.rest import Client

BASE_URL = '35.208.177.121:8000'

weekday_names = ( 'Monday' , 'Tuesday' , 'Wednesday' , 'Thursday' , 'Friday' , 'Saturday' , 'Sunday' )

parser = argparse.ArgumentParser(description='Let us spawn some surveys.')
parser.add_argument('--studyid', type=int, help='Which study should we spawn surveys for?' , default=1 )
parser.add_argument('--duration', type=int , help='Number of days the survey is valid for.' , default=2 )

args = parser.parse_args()

def dt_to_django( dt_in ):
    return dt_in.strftime( '%Y-%m-%d %H:%M:%S' )
def dt_to_human( dt_in ):
    # return weekday_names[ dt_in.weekday() ] + " at " + dt_in.strftime( ' %H:%M' )
    return dt_in.strftime( '%A at %I:%M %p' )

def generate_token( existing_tokens ):
    while True:                # keep generating until a unique one is found
        token = functools.reduce( lambda x,y: x+y , random.choices( string.ascii_lowercase + string.digits , k=6 ) )
        if token not in existing_tokens:
            return token

# Your Account SID from twilio.com/console
account_sid = "AC6f01e296408ba99c27337463dd167164"
# Your Auth Token from twilio.com/console
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

result = c.execute( 'SELECT * FROM surveys_user WHERE studyID_id=? AND active_p=true' , ( args.studyid , ) )
user_records = [ r for r in result ]

#
# grab all factors for the supplied study id
#

result = c.execute( 'SELECT * FROM surveys_factor WHERE studyID_id=?' , ( args.studyid, ) )
factor_records = [ r for r in result ]

#
# for each factor, grab all candidate question texts
#

factor_question_records = {}
for factor in factor_records:
    result = c.execute( 'SELECT * FROM surveys_question_text WHERE factorID_id=?' , ( factor[0], ) )
    factor_question_records[ factor[0] ] = [ r for r in result ]

#
# for each user ...
#

for user in user_records:

    #
    # for each factor, select a question text
    #

    selected_questions = []
    for factor in factor_records:
        selected_question_idx = random.choice( range( len(factor_question_records[ factor[0] ] ) ) )
        selected_questions += [ factor_question_records[ factor[0] ][ selected_question_idx ] ]
        
    #
    # create a survey request record
    # * create the start / end date-times
    # * generate a unique token
    # * insert into DB
    #
    timezone = datetime.timezone( datetime.timedelta( hours=-6 ) )
    start_dt = datetime.datetime.now( timezone )
    end_dt = datetime.datetime.now( timezone ) + datetime.timedelta(days=args.duration)
    # end_dt = end_dt.replace( hour = 23 , minute=59 , second=59 )

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
    # add the questions to the table
    #

    for question in selected_questions:
        result = c.execute( 'INSERT INTO surveys_question ( questionTextID_id , surveyID_id) VALUES ( ? , ?)' ,
                            ( question[0] , new_survey_id ) )
    conn.commit()

    #
    # send SMS with survey request
    #

    try:
        message = twilio_client.messages.create(
            to='+1'+user[2] ,
            from_='+16072282179',
            body='What\'s up, ' + user[1] + '? You can take your survey at: http://'+BASE_URL+'/surveys/'+token+' Your survey will expire on ' + dt_to_human( end_dt ) + '.' )
        print( 'SMS sent to user' , user[0] , user[1] , 'at' , user[2] )
    except Exception as e:
        print( 'Recieved exception when sending survey request URL.' , e )
        print( 'Error when sending SMS sent to user' , user[0] , user[1] , 'at' , user[2] )

#
# ... end for each user
# 

conn.close()
