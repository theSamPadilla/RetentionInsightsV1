import random , datetime , random , string
import sqlite3
from twilio.rest import Client

BASE_URL = '34.123.64.125:8000'

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

study_id = 1

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

result = c.execute( 'SELECT * FROM surveys_user WHERE studyID_id=?' , ( study_id, ) )
user_records = [ r for r in result ]

#
# grab all factors for the supplied study id
#

result = c.execute( 'SELECT * FROM surveys_factor WHERE studyID_id=?' , ( study_id, ) )
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
    end_dt = datetime.datetime.now( timezone ) + datetime.timedelta(days=2)
    end_dt = end_dt.replace( hour = 23 , minute=59 , second=59 )

    token = generate_token( existing_tokens )
    existing_tokens += [token]

    result = c.execute( 'INSERT INTO surveys_survey (completed_p , userID_id , expirationDate , date , token ) VALUES (False , ? , ? , ? , ?)' ,
                        ( user[0] , datetime.datetime.now().isoformat() , ( datetime.datetime.now() + datetime.timedelta(days=2) ).isoformat() , token ) )
    conn.commit()
    new_survey_id = c.lastrowid

    #
    # add the questions to the table
    #
    for question in selected_questions:
        result = c.execute( 'INSERT INTO surveys_question ( questionTextID_id , surveyID_id) VALUES ( ? , ?)' ,
                            ( question[0] , new_survey_id ) )

    #
    # send SMS with survey request
    #
    try:
        message = twilio_client.messages.create(
            to='+1'+user[2] ,
            from_='+16072282179',
            body='Please take a survey at: http://'+BASE_URL+'/surveys/'+token+' Your survey will expire at midnight on ' + end_dt.date().isoformat() )
    except Exception as e:
        print( 'Recieved exception when sending survey request URL.' , e )

#
# ... end for each user
# 

conn.close()
