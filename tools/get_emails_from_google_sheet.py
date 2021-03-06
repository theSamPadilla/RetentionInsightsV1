import csv
import sqlite3

STUDY_ID = 2


#
# grab all the users currently in the system
# 

users = {}
with open('/home/dane/Morningside_accepted_2021_03_01.csv') as infile:

    csv_reader = csv.reader( infile )

    for row in csv_reader:

        phone_num = row[3]
        phone_num = phone_num.replace( '(' , '' )
        phone_num = phone_num.replace( ')' , '' )
        phone_num = phone_num.replace( '-' , '' )
        phone_num = phone_num.replace( ' ' , '' )

        if len(phone_num)==10 and phone_num.isdigit() and phone_num not in users :
            users[ phone_num ] = { 'name' : row[1] , 'email' : row[2] , 'class' : row[4] }
        else:
            print( "Skipping" , row )


#
# grab all the users currently in the system
# 

conn = sqlite3.connect( '/home/sam/RetentionInsightsV1/RetentionInsights/db.sqlite3' )
c = conn.cursor()
result = c.execute( 'SELECT * FROM surveys_user WHERE studyID_id=?' , ( STUDY_ID, ) )
db_phones = [ r[2] for r in result ]

#
# insert user into table if not already in the system
# 

for users_phones in users.keys():

    if users_phones not in db_phones :

        result = c.execute( 'INSERT INTO surveys_user ( firstName , phoneNumber , email , userGroup , studyID_id , active_p ) VALUES (? , ? , ? , ? ,? , True)' ,
                        ( users[users_phones][ 'name' ] ,
                          users_phones ,
                          users[users_phones][ 'email' ] ,
                          users[users_phones][ 'class' ] ,
                          STUDY_ID ) )

        new_user_id = c.lastrowid
        result = c.execute( 'INSERT INTO surveys_reward ( userID_id , streakPoints , weeklyResponses , totalResponses ) VALUES ( ? , 0 , 0, 0 )' ,
                        ( new_user_id , ) )

        print( "Inserted " , users[users_phones] )

    else:

        print( "Skipping " , users[users_phones] )

conn.commit()
conn.close()
