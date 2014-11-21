# Slimmemeterportal scraper

## About

This short script provides a way to get the data from slimmemeterportal into my own database, because they didn't offer an API.

## Usage

First hook op the Peewee model to the database by changing this line:

    db = peewee.MySQLDatabase("database_name", host="localhost", user="root", password="password")

Then run in an interpreter:

    import scraper
    setup()

That creates the necessary tables in the database and should on be run once. From now on you just call:

    import scraper
    scrape(unix_timestamp, email, password)

## Dependencies

- Peewee
- Mechanize
- xlrd (for the excel sheets)

## Future

- Increase commandline ease of use
- Store the auth details in a pickled file or something
- Move to a class based scraper
