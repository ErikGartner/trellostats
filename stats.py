# Designed for python27
from trollop import TrelloConnection
import sys
import os
import json
import copy
import csv
from datetime import datetime, date, time, timedelta
import pytz
import isodate
import pickle
import time
import plotly.plotly as py
from plotly.graph_objs import *

def writecsv(filename, indata, conn):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        keys = sorted(indata.keys())
        # headers
        list_keys = list(indata[keys[0]].keys())
        header = ['Date']
        for key in list_keys:
            header.append(conn.get_list(key).name.encode("ascii","ignore"))

        writer.writerow(header)
        # data
        for key in keys:
            data = indata[key]
            row = [key]
            for x in list_keys:
                if x in data:
                    row.append(data[x])
                else:
                    row.append(0)
            writer.writerow(row)


try:
  with open('settings.json', 'r') as myfile:
      settings = json.load(myfile)
      app_key = settings['app_key']
      user_key = settings['user_key']
      board_id = settings['board']
      milestones = settings['milestones']
except:
    print('Error while reading settings.json')
    sys.exit()

conn = TrelloConnection(app_key,user_key)
board = conn.get_board(board_id)

# copy all lists current form
lists = {}
for lst in board.lists:
    lists.update({lst._data['id']: len(lst.cards)})
history = {datetime.now(pytz.utc): lists}

# start creating the history
lists = copy.deepcopy(lists)
sorted_boards =  sorted(board.actions, key=lambda x: x.date, reverse=True)
print('Retrieved %d actions for %s. Oldest from %s' % (len(sorted_boards), board.name, sorted_boards[-1].date))

# pickle raw data for backup purpose and future use.
back_time = str(int(round(time.time() * 1000)))
with open('backup/' + back_time + '_actions', 'w') as myfile:
    raw_action_data = map(lambda a: a.data, sorted_boards)
    pickle.dump(raw_action_data, myfile)

for action in sorted_boards:

    if action.type == 'createCard':
        lst = action.data['list']['id']
        lists[lst] = max(lists[lst] - 1,0);

    elif action.type == 'updateCard':
        if 'listBefore' in action.data:
            old_lst = action.data['listBefore']['id']
            new_lst = action.data['listAfter']['id']
            if not old_lst in lists:
                lists[old_lst] = 0
            lists[old_lst] = lists[old_lst] + 1
            lists[new_lst] = max(lists[new_lst] - 1,0)

    elif action.type == 'convertToCardFromCheckItem':
        lst = action.data['list']['id']
        lists[lst] = lists[lst] - 1;

    elif action.type == 'deleteCard':
        lst = action.data['list']['id']
        lists[lst] = lists[lst] + 1

    elif action.type == 'createList':
        lists[action.data['list']['id']] = 0

    else:
        # We don't handle every event
        pass

    history.update({action.date: lists})
    lists = copy.deepcopy(lists)

# write raw data to csv
writecsv('rawdata.csv', history, conn)

# compress to milestone
milestone_states = {}
keys = sorted(history.keys())
for milestone in milestones:
    milestone = isodate.parse_date(milestone)

    while len(keys) > 0 and keys[0].date() < milestone:
        key = keys.pop(0)
        milestone_states.update({milestone: history[key]})
if len(keys) > 0:
    milestone_states.update({datetime.now(pytz.utc).date(): history[keys[-1]]})
writecsv('milestonedata.csv', milestone_states, conn)
