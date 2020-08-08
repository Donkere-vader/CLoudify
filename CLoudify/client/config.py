import json

f = json.load(open('.cloudify_settings.json'))

IP = f['ip']
PORT = f['port']
AUTH_KEY = f['auth_key']
SYNC_FOLDER = f['sync_folder']