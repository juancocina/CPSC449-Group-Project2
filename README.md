# CSPC449-Group-Project2

# Member (turned into a solo project)
- Juan Cocina

# Files includes
- /bin/init.sh
- /bin/init_timeline.sh
- 
- /etc/haproxy.cfg
- /etc/logging.ini
- /etc/timeline.ini
- /etc/users.ini
- 
- /share/followers.csv
- /share/timeline.json
- /share/timeline.csv
- /share/user.json
- /share/user.csv
- 
- /var (folder will be empty)
- .env
- Procfile
- README.md
- 
- timelines.py
- users.py

# How to run
(download the folder)
once inside the folder on your machine run ./bin/init.sh to create a database
DO NOT, cd into bin to run init, the DB won't be made

run ./bin/init_timeline.sh for the timelines DB

Run: hug -f timelines.py or hug -f users.py

or

Run: foreman start -m users=1,timelines=3 -p 8000
to start 1 user service and 3 timelines service
The foreman response will tell you specifically which ports the services are on

# User Calls
(in browser, assume localhost:8000)
- /users/ will display all the users in the DB
- /users/?username=insert_username_here will search for a user
- /followers/ will display who follows who
- /followers/follower_id=a_number&following_id=a_number will add followers
- /authenticate/username=user_name&password=password will return 200 or 404 depending on if the user is in the DB with
the correct password

- (in the cli...) http POST localhost:8000/users/ username=test email=test@example.com password=pass bio='a bio' 
***I couldn't figure out this post in the browser


# Timeline Calls
(in browser, assume localhost:8000)
- /timelines/ displays the public timeline
- /timelines/?username=user_name will display a specific user's posts
- (in the cli...) http POST localhost:8000/timelines/ username=user_name text='text text text/' *** this will create a user. Couldn't figure it out in the browser.


# Missing 
- authenticate from timelines.py (but can in users.py)
- repost
- fetch timeline from people you follow
- delete
- HAProxy configuration (file exists, but couldn't get it running)
- load balancing


