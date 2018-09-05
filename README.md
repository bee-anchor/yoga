# FAF - Flexible Automation Framework
An automation library that will do a lot of the heavy lifting for you around test configuration and UI test driver setup, but leave flexibility!
Flexibility to choose your own test runner, to expand the library, write tests how *you* want and more!
# Getting started
1. Create a new project for your tests
#### Project structure:
```
~/project-autoamted-tests
    /tests
        test.py
    /pages
        page.py
    local_capabilites.ini
    config.ini
    run.py
```

1. Clone faf
```
git clone git@bitbucket.org:infinityworksconsulting/faf.git
```
1. Install faf as a dependency for your project using pip (highly recommend you use a virtual env!)
```
cd project-automated-tests
source venv
pip install /path/to/faf/setup.py
```
1. Copy the config from `faf/resources/example_config.ini` to your `config.ini` in your project, and change the values to those for your project.
1. Copy one of the example runners from `faf/resources` to your `run.py` file (the pytest one is currently best supported and tested)
1. Start writing tests!
1. Run your tests e.g. locally with
```
python3 run.py -e test -x selenium_local -b chrome   
```
    
##The config.ini
* `environment.env` sections will be reduced to just one, called `environment`, which will contain the env config for the env specified at runtime
* anything in the config will be available to you during tests via the `CONTEXT.config` object
* can add anything you may need to the config, just don't remove any of the required items

##The local_capabilities.ini
* stores capabilities for running appium tests locally, add these as required, these is an example on in `resources`

# TODO

* after test actions
* how to add other test runners support
* how to contribute
    
