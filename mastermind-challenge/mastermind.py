import requests, json, sys


email = ''
r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
headers = r.json()
headers['Content-Type'] = 'application/json'

level=1
# Interacting with the game

print(f'Gathering level {level}...\n')
r = requests.get(f'https://mastermind.praetorian.com/level/{level}/', headers=headers)
print(r.json())
# > {'numGladiators': 4, 'numGuesses': 8, 'numRounds': 1, 'numWeapons': 6}
guess = [1,2,3,4]
r = requests.post(f'https://mastermind.praetorian.com/level/{level}/', data=json.dumps({'guess':guess}), headers=headers)
print(r.json())
# > {'response': [2, 1]}