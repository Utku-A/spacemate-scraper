import os

Agent_List_Scanner  = os.environ.setdefault('Agent_List_Scanner', 'Ready')
Agent_Page_Scanner  = os.environ.setdefault('Agent_Page_Scanner', 'Ready')
Search_Location     = os.environ.setdefault('Search_Location', 'None')
Search_Query        = os.environ.setdefault('Search_Query', 'None')


db_config = {
    "user": "spacemate",
    "password": "spacemate_321123",
    "host": '31.223.4.248',
    "port": 3306,
    "database": "Spacemate"
}
