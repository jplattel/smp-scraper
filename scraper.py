import logging
import sys
import os
import mechanize
import xlrd
import csv
import datetime
import peewee

# Database
db = peewee.MySQLDatabase("database_name", host="localhost", user="root", password="password")

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Usage(BaseModel):
    date = peewee.DateTimeField(unique=True)
    value = peewee.FloatField()

def setup():
    db.connect()
    db.create_table(Usage)

# Logging
logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

def scrape(date=1416265200, email, password):
    """
    Scrapes data from slimmemeterportal.nl
    """

    # Open browser
    br = mechanize.Browser()
    br.open('https://slimmemeterportal.nl/login')

    # Fill out login form
    br.select_form(nr=0)
    br["user_session[email]"] = email
    br["user_session[password]"] = password
    br.submit()

    # Download the XLS file with
    r = br.retrieve('https://slimmemeterportal.nl/cust/consumption/chart.xls?commodity=power&datatype=consumption&range=86400&timeslot_start=' + str(date), str(date) + '.xls')

# Save from excel to database
def save_to_db(date):
    wb = xlrd.open_workbook(str(date) + '.xls')
    sh = wb.sheet_by_name('Sheet 1')

    r = range(sh.nrows)
    r.pop(0) # remove header

    for rownum in r:
        # convert datatime from excel
        d = xlrd.xldate_as_tuple(sh.row_values(rownum)[0], wb.datemode) # Convert Excel data to tuple
        d = datetime.datetime(*d) # tuple to datetime

        # Ugly way to check if it entry exists in the database, quick 'n dirty!
        e = False
        try:
            e = Usage.get(Usage.date == d)
        except:
            pass
        if not e:
            u = Usage(date=d, value=sh.row_values(rownum)[1])
            u.save()

    # Delete xls file for cleanup
    os.remove(str(date) + '.xls')

# Start scraping
scrape(unix_timestamp_at_midnight_of_a_day, email, password)
save_to_db(unix_timestamp_at_midnight_of_a_day)
