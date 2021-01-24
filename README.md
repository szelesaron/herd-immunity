# herd-immunity

Website to display expected date of herd immunity.

* Covid.py gets data from https://github.com/owid/covid-19-data/tree/master/public/data and calculates 14 day average of daily vaccinations. Builds a dataframe object and creates a csv file.
* db.py creates the database, reads in the csv file and insert the data into the database
