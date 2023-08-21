import requests

car = {
    'brand': 'ford', 
    'title_status': 'clean vehicle', 
    'state': 'tennessee', 
    'year': 2015, 
    'mileage': 19052
}


host = 'localhost:9696'
# host = '.....elasticbeanstalk.com'

url = f'http://{host}/predict'

response = requests.post(url, json=car)
print(response.json())