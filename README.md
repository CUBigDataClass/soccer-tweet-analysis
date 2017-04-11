# Party Parrots

[![Build Status](https://travis-ci.com/CUBigDataClass/Party-Parrots.svg?token=Q3z6q2gUKeig35zmUNn2&branch=master)](https://travis-ci.com/CUBigDataClass/Party-Parrots)

### Project Structure
* A Django app. This serves as the frontend for the main application

### Requirements
* Have `node.js` installed
* Recommended to use a virtualenv

### Building the project
* Install the python requirements. `pip install -r requirements.txt`
* Run `python setup.py develop`
* Install the frontend requirements. `npm install`
* Install the frontend components. `bower install`
* Build the frontend components. `node_modules/grunt/bin/grunt build_bower`

### Running the project
* Run `./manage.py runserver`
