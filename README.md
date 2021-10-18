# CSPC449-Group-Project2

# Members
- Juan Cocina
- Tilak ghorashainee

# How to run
download the repository
once inside the folder on your machine run ./bin/.init.sh to create a database
DO NOT, cd into bin to run init, the DB won't be made

then hug -f users.api will start a local server
localhost:8000

localhost:8000/users/ should show the base users
in the database

to add a user to the database
http POST localhost:8000/users/ username=test email=test@exampe.com password=testing bio=this%20is%20a%20test
in the terminal
spaces in a POST call must be entered as "%20"

to search for a user
http GET localhost:8000/search?username=*insert name here*
in the terminal

