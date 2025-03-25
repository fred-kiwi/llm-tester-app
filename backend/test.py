import os
import requests

os.system('clear')

testBody = {
    "text": "What is your favourite animal and why?"
    }

endpointTest = requests.post(url="http://0.0.0.0:8000/chat", json=testBody)

print(endpointTest)
print(endpointTest.json())