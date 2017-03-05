# Party Parrots

[![Build Status](https://travis-ci.com/CUBigDataClass/Party-Parrots.svg?token=Q3z6q2gUKeig35zmUNn2&branch=master)](https://travis-ci.com/CUBigDataClass/Party-Parrots)

### Project Structure
This project is built in two parts.
* A Django app. This serves as the frontend for the main application
* React app. This is a server app which compiles React components into ES5.

### Requirements
* Have `node.js` installed
* Recommended to use a virtualenv

### Building the project
* Install the python requirements. `pip install -r requirements.txt`
* Install the frontend requirements. `npm install`

### Running the project
* Open two terminals.
* Run `./manage.py runserver` in the first
* Run `node server.js` in the second. This terminal is for hot encoding of react components
