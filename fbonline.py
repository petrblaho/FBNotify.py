import requests
import json
import subprocess
import time
ACCESS_TOKEN = "ENTER YOUR ACCESS TOKEN"
friends_online = set()
DEBUG = False

def get_friends_online():
    '''Returns friends who are online'''
    query = ("SELECT uid, name FROM user WHERE online_presence IN ('active', 'idle') AND uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")

    payload = {'q' : query, 'access_token' : ACCESS_TOKEN }
    r = requests.get('https://graph.facebook.com/fql', params=payload)
    result = json.loads(r.text)
    if DEBUG: print(result)
    friends = set()
    for name in result['data']:
	    friends.add(name['name'])
    return friends

while 1:
    last_friends_online = friends_online.copy()
    friends_online = get_friends_online()
    new_friends_online = friends_online - last_friends_online
    new_friends_offline = last_friends_online - friends_online
    for friend in new_friends_online:
        message = "%s is online" % friend
        subprocess.Popen(['notify-send', message])
    for friend in new_friends_offline:
        message = "%s is offline" % friend
        subprocess.Popen(['notify-send', message])
    time.sleep(60)
