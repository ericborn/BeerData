# BeerData
Learning PostgreSQL by importing a beer review data set with Python

I wrote the following code while learning PostgreSQL and psycopg2, which is the Python database adapter.
The code creates a database and table in Postgres using the psycopg2 package,
Reads and clean a csv file using pandas and finally inserts the clean data into the database using Python with open.

The dataset I used is comprised of beer reviews from a website called Beeradvocate.com. The data spans a period of more than 10 years, 
and has more than ~1.5 million rows. The original dataset file is 171MB, much too large to include on git, so I built the program 
to download the file straight into a dataframe from the URL, but this will take some time depending on your internet connection.
If you do not want to download the full file I have included a condensed version with less rows that is zipped. 
You can also download the full here: https://query.data.world/s/rn36f5pg4uccomqwkn6ovfsrbgw37i which will allow you to use the full set without having keep downloading it.

You will need PostgreSQL installed either locally or on a server prior to utilizing this program. 
I used a local instance and the default account, postgres, to make connections with a password of 1234. 
This user can be edited within the program at in the database.ini file if you wish to use different credentials or connect to a remote server.

Place the files in the a directory and execute the main.py, the rest should take care of itself and your data should be accessable in Postgres within a few minutes.

Happy exploring!
