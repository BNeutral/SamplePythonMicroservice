# SamplePythonMicroservice

A sample python microservice to show some minimal skills. Lots of security and other issues making this not production ready by a long shot, but it's done according to some specification to be coded quickly.

# Setup

Install python3 so it's accessible via the command line.

Install virtual environments for python if you don't have them set up (venv)

# running / testing

## Windows

In a powershell run the following

> ./run_debug.ps1

Server should be up and listening, ip/port will be shown in the console.

You can acces the url:port/docs to easily test the API.

You can also acces the url:port/redoc to check out the API docs in a non interactive manner.

For looking at the sqlite DB just use a client of your choice.

## Linux

Same as above but run the bash (.sh) versions of the scripts.

# To do list

Since it's just a quick exercise there's a lot of things that are just badly done due to time constrains. Ideally we'd be doing the following:
* Proper input validation
* Authentication
* Use a proper DB
* Async (and db conneciton pooling)
* Automated tests with adversarial cases
* Monitoring
* Hooks to report issues
* Separate code into various files
* Server logs (don't forget to set them rotating)
* Dockerize
* Better enum handling so the messages we get/send have them as readable strings
* Etc

# Code conventions

Install pylint and set it up for your IDE. Use the full linting, some editors like VScode set you up for minimal linting.

# Contributing

If you add packages, you should run 

> pip freeze > requirements.txt

So people can install the libraries with the following (will need to update scripts)

> pip install -r requirements.txt
