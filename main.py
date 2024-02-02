import requests
from flask import Flask, request

app = Flask(__name__)

# Set your Trakteer.io API token
TRAKTEER_API_TOKEN = 'trstream-I4vhLh0IDil4rsBQLQ6Q'

# Set your Servertap.io API token
SERVERTAP_API_TOKEN = '1234'

def execute_command(command):
    url = 'http://192.46.224.97:4567/v1/server/exec'
    headers = {'Authorization': f'Bearer {SERVERTAP_API_TOKEN}'}
    data = {'command': command}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

@app.route('/trakteer-webhook', methods=['POST'])
def trakteer_webhook():
    data = request.json
    amount = data.get('data', {}).get('attributes', {}).get('amount', 0)
    name = data.get('data', {}).get('attributes', {}).get('user', {}).get('name', 'Anonymous')
    message = data.get('data', {}).get('attributes', {}).get('message', '')
    if amount >= 10000:
        execute_command(f'/say Terima kasih {name} atas donasinya sebesar {amount}! Pesan dari donatur: {message}')
    elif amount >= 5000:
        execute_command(f'/say Terima kasih {name} atas donasinya sebesar {amount}!')
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)