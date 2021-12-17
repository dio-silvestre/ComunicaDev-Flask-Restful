# Welcome to Comunica Dev API

The Comunica Dev API is a aplications based on SQL and Flask, to manage the Comunica Dev application.

To use follow the instructions below.

The entire application is contained within the `app` folder.

`requirements.txt` is a colletction with all frameworks needed to run te aplication.

The `migrations` folder heave the database configs.

IMPORTANT: Don't forget populate your `.env` file according the `.env.example` file.


    [ BASE URL: https://comunica-dev-api.herokuapp.com/api ]
# 
## Install
After cloning the project and accessing the directory, create and start your virtual environment:
    
    python -m venv venv --upgrade-deps
    
    source venv/bin/activate

To init the aplication run those commands in your terminal and after that start your virtual enviroment:

    pip install -r requirements.txt
##
    flask db upgrade

## Run the app

    flask run

#
# Docs
Below you will find the endpoints divided by the api sessions:


- [Users](./documentation/users.md)
- [Address](./documentation/address.md)
- [Categories](./documentation/categories.md)
- [Leads](./documentation/leads.md)
- [lessons](./documentation/lessons.md)
- [captchas](./documentation/captchas.md)

