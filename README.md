# CSPC449-Group-Project2

# Members
- Juan Cocina
- Tilak ghorashainee

# How to run
download the repository
once inside the folder on your machine run ./bin/.init.sh to create a database

then hug -f users.api will start a local server
localhost:8000

localhost:8000/users/ should show the base users
in the database

to add a user to the database
http POST localhost:8000/users/ username=test email=test@exampe.com password=testing bio=this%20is%20a%20test
in the terminal