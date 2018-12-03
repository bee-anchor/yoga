# FAF - Flexible Automation Framework
An automation library that will do a lot of the heavy lifting for you around test configuration and UI test driver setup, but leave flexibility!
Flexibility to choose your own test runner, to expand the library, write tests how *you* want and more!

# Getting started

### Requirements
* python 3.6 or later
* pip

### Setup

1. Create a new project for your tests
#### Project structure:
```
~/project-automated-tests
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
pip install /path/to/faf/setup.py
```
1. Copy the config from `faf/resources/example_config.ini` to your `config.ini` in your project, and change the values to those for your project.
1. Copy one of the example runners from `faf/resources` to your `run.py` file (the pytest one is currently best supported and tested)
1. Start writing tests
1. Run your tests! e.g. locally with
```
python3 run.py -e test -x selenium_local -b chrome   
```
    
## The config.ini
* This uses python's standard INI file format with the configparser library.
* Config is divided into sections (denoted by text in square brackets) and the key value pairs belonging to those sections.
* All sections and key value pairs in the example config are required, although technically only one environment section is actually required (but the two defined will be wanted in most cases).
* All config values can be accessed within tests via the `CONTEXT.config` object e.g. `CONTEXT.config[<section>][<key>]`.
* The multiple `environment.env` sections in the INI file will be reduced to just one called `environment` at runtime, which will contain the env config for the env specified and is therefore accessed by just `CONTEXT.config['environment'][<key>]`.
* You can add anything you may need to the config, just don't remove any of the required items.
* Environment variables can be used in the config values using interpolation, with syntax of `${}`. e.g. `key = testvaluewith${interploated}`

## The local_capabilities.ini
* Stores capabilities for running appium tests locally, add these as required. There is an example one in `resources`

## Run framework tests
These are pytest tests, run the pytest command in the faf root directory:
```
cd /faf
pytest
```

# Writing tests

You can write tests it whatever way you want, for the test runner you are using. Some libraries are installed as part of faf which you will find useful:
* colorama - allows you to colour text on the console
* assertpy - more powerful assertion library which will give you useful error messages when assertions fail
* pdbpp - a better python debugger that will automatically be used in place of pdb - it has autocomplete!

### After test actions

You will need to do some manual setup for you tests to support saucelabs test runs and slack reporting, in the form of actions that are taken at the end of the test run. This will depend on the test runner you use, and how it can support it.
For pytest, you can use it's hooks and fixtures to do the actions. The example code you will need is:

```python
results = []

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # hook to handle actions to take when test outcomes are available
    # stores test outcomes in array
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        results.append(rep.outcome)

@pytest.fixture(scope="session", autouse=True)
def end_of_test_actions():
    # if the test is running in a remote mode and there is a failure, report job failed to saucelabs and slack
    # if all tests passed, report job passed to saucelabs
    # without this the job remains in an unknown state on saucelabs
    yield
    if CONTEXT.args.execution in {'selenium_remote', 'appium_remote'}:
        if 'failed' in results:
            SauceHelper().report_outcome(CONTEXT.driver.session_id, False)
            if CONTEXT.args.slack_report:
                SlackReporter(CONTEXT.config['slack']['webhook']).report_test_failure()
        else:
            SauceHelper().report_outcome(CONTEXT.driver.session_id, True)
```
The critical part is that you report the job outcome to saucelabs and slack when it is appropriate


# Running Automation Tests

## Command line arguments

* There are a number of command line args which are required by the framework, and a number that are specific to each test runner.
* The arguments required vary a little depending on where you are wanting to run tests.

#### The 'base' arguments:

| Arg | Required | Description|
|:----|:-------- |:-----------|
| -c --config |no| path to the config file to use, defaults to `config.ini` |
| -e --environment |yes| environment to run tests in, must have a section in the config.ini |
| -x --execution |yes| execution type, one of selenium_local, selenium_remote, appium_local, appium_remote, grid_local, non-ui|
| -b --browser |yes - with selenium_local execution type| browser to run tests on (if not using non-ui execution type) one of chrome, firefox, internet explorer, safari, edge|
| -p --capabilities |yes - with appium or remote execution types|  which capabilities to use from relevant capabilities file (remote/local) when running using remote or any appium execution type|
| -l --local_capabilities_file |no| path of local capabilities file, if overriding from the default of local_capabilities.ini |
| -s --slack_report |no| turn on slack reporting of test outcomes|
| -o --override |no| config value override e.g. -o section.option=value section.option2=value2. Overrides after environment config modifications, so to override env url would be e.g. local.url=https://app.test|
| -d --debug |no| run in debug mode - will drop you into debugger on test failure. DO NOT USE ON CI! |

#### Pytest specific arguments:

| Arg |Required| Description|
|:----|:-------|:----------|
| --test-dir |no| path to tests, default is |
| -k |no| keyword filter, to only run test containing this string in their name|
| -m |no| mark filter, to only run tests that are marked as the pattern used dictates|

## Running tests (assuming using pytest runner)

### Example commands:

|command|description|
|-------|-----------|
|`python3 run.py -e test -x selenium_local -b chrome`| run locally on chrome|
|`python3 run.py -e test -x selenium_local -b chrome -d -k login_logout`| run locally on chrome in debug mode where tests contain 'login_logout' in their name|
|`python3 run.py -e test -x selenium_local -b chrome -d -m desktop`| run locally on chrome where tests are marked with 'desktop'|
|`python3 run.py -e test -x appium_local -p iphone7`|run tests locally using appium, on the device specified in the local_capabilities.ini file as 'iphone7' (appium and the correct simulator need to be running first)|
|`python3 run.py -e test -x grid_local -b "internet explorer"`|run test on an internet explorer browser connected to a locally running selenium grid (can use this to run tests on virtual machines)|
|`python3 run.py -e test -x selenium_remote -p windows10chrome -s`|run test remotely on saucelabs using the remote capabilities specified by the windows10chrome section, and report a test failure to slack|
|`python3 run.py -e test -x appium_remote -p android6`|run test remotely on saucelabs using the remote capabilities specified by the android6 section|

# Adding to FAF

As this is a library shared by multiple projects, any new code must be submitted via a PR!
Generally most code changes should need to happen in the browser.py file only.

## Adding more test runners

Currently the pytest runner is the only one is use in any projects, the nose runner has been used in the past, but the behave runner is not yet in a working state.

Add the commandline arguments required, pass these through to the main method of the runner.

Add the example runner file to the resources directory and make sure to return the correct exit code from the runner, else CI won't know the test outcome (`sys.exit(code)`)




    
