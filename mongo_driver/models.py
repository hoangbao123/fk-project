from pymongo import MongoClient

#Parameters to connect to the MongoDB server
#Two connection simultaneous access might be needed at times

#This is where my CoreNLP server is hosted.
#It will be running throughout the evaluation time
#In case there are any issues, you might want to run you own
#CoreNLP server and replace the address here
MongoHost = '34.87.20.130'
MongoPort = 27017

client = MongoClient('mongodb://'+MongoHost+':'+str(MongoPort)+'/test')
client2 = MongoClient('mongodb://'+MongoHost+':'+str(MongoPort)+'/test')

db=client['test']
db2=client2['test']

# Check Connection
print(db.client)