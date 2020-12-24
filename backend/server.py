from flask import Flask
import requests
import json
from time import sleep
from datetime import datetime
from threading import Thread

app = Flask(__name__)

ru_rating = 0
world_rating = 0
pts = 0

def update():
    global ru_rating, world_rating, pts
    while True:
        data = json.loads(requests.get('https://icyftl.ru/ctftime/teams/get/team/121175/id').text)
        ru_rating = data.get('country_place')
        if data.get('rating'):
            world_rating = data['rating'][0][str(datetime.now().year)]['rating_place']
            pts = 0
            for x in data['rating']:
                for key in x:
                    pts += int(x[key]['rating_points'])
        sleep(86400)


Thread(target=update).start()


@app.route('/info', methods=['GET'])
def show():
    global ru_rating, world_rating, pts
    return json.dumps({'ru_rating': ru_rating, 'world_rating': world_rating, 'pts': pts})


app.run('localhost', 8013, False)
