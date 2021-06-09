
# First time Setup

## create a virtual environment if desired

The default python version may be fine, but this was tested with python3.8

`virtualenv demoenv -p /usr/bin/python3.8`

`cd demoenv/bin`

`source activate # or use what is appropriate for your shell`

`cd ../..`

## install needed packages

`python -m pip install -r requirements.txt`

## Start the rasa server

`docker-compose up rasa`

it will download some images the first time.  Then it will take a minute before it is ready for requests

## Run the notebook

open rasaDemo.ipynb and run

