# CitizenV.server
2122I_INT3306_1

## Install
* Install ```python3```
* Then install required modules with this command
```bash
pip install -r requirements.txt
```

## Setup
* Change ```app.config['SQLALCHEMY_DATABASE_URI']``` to your local MySQL connection URI in ```citizenV.py```

* Enable IMAP and allow less secure app in your Gmail account 

* Change ```MAIL_USERNAME``` and ```MAIL_PASSWORD``` to your Google account, and ```JWT_SECRET_KEY``` as you like in ```src.core.config.py``` file

* Change ```sender``` part in line ... of file ```src.controller.account.py``` to your mail address

* Change ```sender``` part in line ... of file ```src.controller.account_management.py``` to your mail address

* Change ```sender``` part in ```send_mail``` function of file ```src.services.progressService.py``` to your mail address

* Create a ```citizenv``` database in your MySQL server, then import schema file ```citizenv.sql``` and data file ```data.sql```

* You can see accounts id (which is also the username) in the database, all have ```123456``` as the default pass

## Run
``` python citizenV.py```

## Project structure
```
src---
  |  |- controllers // routes
  |  |- services // validate datas and interact with model layer
  |  |- models // interact with database, query and return query result, insert, update, delete
  |  |- core // core config of this app, including authorization module and secret keys
  |- citizenv.py // main running file
  |- database.py // connecting flask to MySQL database
```

### Small notification
PyJWT 1.7.1 or 2.3.0
