# MeetFriendBot

To run project locally:

1) Make virtualenv with python 3.5+

2) Install requirements

3) Install postgres

4) $ sudo -u postgres createdb <db_name>
   $ sudo -u postgres psql <db_name>
       <db_name>=# create user <user_name> password '<password>';
       <db_name>=# grant all privileges on database <db_name> to <user_name>;

5) Create '.env' file with env variables (see 'settings.py' for the list of them)

6) Run server:
    (<your_env>)$ python run.py
