# VSPOMS

VSPOMS is an online learning tool to simulate Stochastic Patch Occupancy Models (SPOMs).

This site enables users to simualate scenarios (either uploaded or randomly generated) with user-defined parameters and settings.
These simulations can be visualised in the form of animations and graphs.

## Installation
The live project can be accessed from [this link](https://vspoms.mvls.gla.ac.uk) - though only on the Glasgow University network.
If you wish to install yourself clone the project and run as you would a usual django app.

Pre-requisites:
- Python 3.10.x or later
- pip

Installation instructions:
- On a server (local or remote), navigate to the chosen directory you wish to install VSPOMS
- Clone the repository into this folder using `git clone`
- Create a virtual environment (optional) by running `python -m venv venv` and `source venv/bin/activate`
- Install the requirements by running `pip install -r requirements.txt`
- Migrate by running `python manage.py makemigrations` and `python manage.py migrate`
- Create a superuser with `python manage.py createsuperuser` and enter credentials when prompted
- Run the server with `python manage.py runserver`
- See the server at `127.0.0.1:8000` or at your URL

## Uploading Scenarios
To upload a scenario to the app:
- Open `[YOUR_URL OR 127.0.0.1:8000]/admin` in a browser
- Click on the `+ Add` button next to `Scenarios`
- Fill in the `Name` field and upload a scenario `.csv` file by clicking `Choose File` and choosing the scenario
- Click `SAVE` to finish - the scenario should be displayed on the site after refreshing

## Deployment
Running on a Glasgow University server, using nginx>gunicorn>django.

Followed [this guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04).

## Authors and acknowledgment
VSPOMS is developed by:
- Max Bell
- Roger Luo
- Hamza Shahid
- Daniel Szittya
- Timothy Wang
- Angus Wilson

## License
VSPOMS is licensed under a
Creative Commons Attribution-NonCommercial 4.0 International License.

## Project status

Project is no longer under active development as of 6th April 2023