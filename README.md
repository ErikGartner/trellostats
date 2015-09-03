# TrelloStats
Generates Trello list stats throughout time with support for milestones.

## Installation
To work properly trollop needs to be modified to set request limit of action
from 50 to 1000.

You also needs to create a backup folde were the raw actions are stored.

Example settings.json:
```json
{
    "app_key": "",
    "user_key": "",
    "board": "",
    "milestones": ["2015-04-15", "2015-04-27", "2015-05-05", "2015-05-20", "2015-05-26"]
}
```
Board variable is the board id. Easily found in the board URL.
