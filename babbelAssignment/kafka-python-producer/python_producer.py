from ensurepip import bootstrap
import time
from kafka import KafkaProducer
import json
from bson import json_util

messages = [{
"EventUUID": "d73d8691c6ba47f2b95466ad36d3b3ea",
"UserUUID": "83e6fef6c0ff4f8b919fdacdb1b70cfb",
"EventName": "LessonStarted",
"CreatedAt": "2021-04-08T22:15:55.992605+02:00"
},
{
"EventUUID": "acb73ae754ad4fc4a5c8099f8332b7e3",
"UserUUID": "83e6fef6c0ff4f8b919fdacdb1b70cfb",
"EventName": "LessonStarted",
"CreatedAt": "2021-04-09T06:16:55.992666+00:00"
},
{
"EventUUID": "d73d8691c6ba47f2b95466ad36d3b3ea",
"UserUUID": "83e6fef6c0ff4f8b919fdacdb1b70cfb",
"EventName": "LessonStarted",
"CreatedAt": "2021-04-08T22:15:55.992605+02:00"
},
{
"EventUUID": "b4cb727b349e476085d733d1abaddcb7",
"UserUUID": "650fc9cb143c46549f54c3419765bc81",
"EventName": "LessonFinished",
"CreatedAt": "2021-04-09T10:58:55.992878+02:00"
},
{
"EventUUID": "e188f4db423a488f87cb74edd3bd7162",
"UserUUID": "650fc9cb143c46549f54c3419765bc81",
"EventName": "UserLoggedIn",
"CreatedAt": "2021-04-09T21:30:55.992798+02:00"
},
{
"EventUUID": "e7e1272939b1406597014ca67678dcec",
"UserUUID": "83e6fef6c0ff4f8b919fdacdb1b70cfb",
"EventName": "UserLoggedOut",
"CreatedAt": "2021-04-11T01:59:55.992850+00:00"
}]

# messages = [{
# "EventUUID": "e7e1272939b1406597014ca67678dceg",
# "UserUUID": "83e6fef6c0ff4f8b919fdacdb1b70cfb",
# "EventName": "UserLoggedOut",
# "CreatedAt": "2021-04-09T01:59:55.992850+00:00"
# }]

def produce_meesages(topic):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    for message in messages:
        producer.send(topic,json.dumps(message, default=json_util.default).encode('utf-8'))
    time.sleep(10)
    print(f'messages published to the topic: {topic}')


if __name__ == '__main__':
    topic = "babbel"
    produce_meesages(topic)