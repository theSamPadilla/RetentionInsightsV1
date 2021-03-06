import csv , functools
import sqlite3

STUDY_ID = 2

#
# grab all the users currently in the system
# 

conn = sqlite3.connect( '/home/sam/RetentionInsightsV1/RetentionInsights/db.sqlite3' )
c = conn.cursor()
result = c.execute( 'SELECT * FROM surveys_user WHERE studyID_id=? and active_p=True', ( STUDY_ID, ) )
db_emails = [ r[3] for r in result ]
conn.close()

#
# grab all the users on the waiting list
# 

emails = []
with open('/home/dane/Morningside_waiting_2021_03_01.csv') as infile:

    csv_reader = csv.reader( infile )

    for row in csv_reader:

        email = row[2].strip()
        if email not in emails:
            emails += [ row[2].strip() ]


print( "accepted:" , functools.reduce(lambda x,y: x+','+y , db_emails) )

print( "waiting: " , functools.reduce(lambda x,y: x+','+y , emails) )
