# TrelloStats
*Simple script that outputs the number of cards in each list throughout time.*

## Usage
Set the settings.json as follows:
```json
{
    "app_key": "",
    "user_key": "",
    "board": "",
    "milestones": ["2015-04-15", "2015-04-27", "2015-05-05", "2015-05-20", "2015-05-26"]
}
```
Here ```app_key``` and ```user_key``` is Trello api keys. ```board```is the board
id and ```milestones``` is a list of days that are considered measurement dates.

Run using: ```python stats.py```

## Installation
Simply install all dependencies using pip: ```pip install -r requirements.txt```.

You need to create a backup folder were the raw actions are stored. This is
since Trello only allows for 1000 actions so we store for future use since we
can never get them again from Trello.
