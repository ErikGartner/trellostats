# Designed for python27

from trollop import TrelloConnection
import sys
import os
import json

try:
  with open('settings.json', 'r') as myfile:
      settings = json.load(myfile)
      app_key = settings['app_key']
      user_key = settings['user_key']
except:
    print('Error while reading settings.json')
    sys.exit()

conn = TrelloConnection(app_key,user_key)

print('Calculating stats for boards:')

for board in conn.me.boards:
    print('\t%s:' % board.name)

    for tlist in board.lists:
        labels = {}
        for card in tlist.cards:
            for label in card.labels:
                i = 1
                if label['name'] in labels:
                    i = labels[label['name']] + 1
                labels[label['name']] = i
        print('\t\t- %s: %d' % (tlist.name, len(tlist.cards)))
        for label in labels:
            print('\t\t\t * %s: %d' % (label, labels[label]))
