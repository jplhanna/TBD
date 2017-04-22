# Delphi
Webapp for finding the title of a movie or television show based on answering 10 or less questions about preferences.

# Setup instructions:
If you are using c9, clone TBD to a c9 workspace. Run command python manage.py runserver $IP:$PORT to view the current site.

If you are using a local environment, clone to your local environment, run command 

pip install django

then run

python manage.py runserver {IP or Port of your choice}

# Interacting with database:
Create an admin account, by running command 

python manage.py createsuperuser

Then from the website navigate to {server}/admin. Sign in using the corresponding credentials made for the superuser.

From this webpage you can edit Users, their user data, Movies, and Questions.
This includes adding individual movies, questions, or users, though this is not the recommended manner of doing so.

# Adding more than 1 movie to the database:
To add add more than 1 movie to the movie table create a csv file of the format

title|webaddress|movie poster adress|object type{movie or show}|popularity score

This csv file must contain movies or shows from available from the same streaming service
Then run command

python manage.py add_movie_data {csv_location} {streaming service}

The streaming service must be in the set [amazon, amazonPrime, googlePlay, hulu, itunes, netflix]

# Adding a question to question list:
To add a question to the database run command

python manage.py add_question {question}

The question must be under 500 characters long and should end with a '?'.