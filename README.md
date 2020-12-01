# wnghub

### 'what's new on github'

### How to use:
- Installation (only tested Python 3.7+): `pip3 install git+https://github.com/brighton1101/wnghub.git@0.0.2`
- Run it! `wnghub` for unread notifications, `wnghub -A` to include read notifications

### Configurable options:
Note that these are all stored to a local config file on your machine. That way, you can set defaults and have these filters pre-applied without having to type out additional info.

#### Exclude or include notifications by:
- repo name
- org name
- notification reason
- type: (pr or issue)

#### And:
- number of results to show
- whether or not to show notifications that are already read
- only show participating

### Example:
```sh
🌴🌴🌴 ~ $ wnghub set-auth <auth token here> # set auth token

🌴🌴🌴 ~ $ wnghub # Run with set configuration (i don't have any unread notifications...)
No new matching notifications!

🌴🌴🌴 ~ $ wnghub -A # shows 'all' notifications (even those that are read)
+-------------------------+----------+------+--------------------------------------------------+
|          Title          |   Repo   | Type |                       url                        |
+-------------------------+----------+------+--------------------------------------------------+
| AuthenticatedUser.ge... | PyGithub |  IS  | https://github.com/PyGithub/PyGithub/issues/1671 |
| Added support for DS... | airflow  |  PR  |   https://github.com/apache/airflow/pull/12467   |
| SSHOperator does sup... | airflow  |  IS  |  https://github.com/apache/airflow/issues/12318  |
| Added `files` to tem... | airflow  |  PR  |   https://github.com/apache/airflow/pull/12435   |
| Add `files` to templ... | airflow  |  IS  |  https://github.com/apache/airflow/issues/12028  |
+-------------------------+----------+------+--------------------------------------------------+

🌴🌴🌴 ~ $ wnghub set-config include_issues false # Turns off showing issues

🌴🌴🌴 ~ $ wnghub get-config include_issues # Gets value of config
False

🌴🌴🌴 ~ $ wnghub get-config --help # View configurable options
Usage: wnghub get-config [OPTIONS] FIELD_NAME

  Gets value from config. Possible values: ['auth_token',
  'show_num_results', 'only_include_repos', 'only_include_orgs',
  'only_include_reasons', 'exclude_repos', 'exclude_orgs',
  'exclude_reasons', 'show_read_results', 'only_include_participating',
  'include_issues', 'include_prs']

Options:
  --help  Show this message and exit.

🌴🌴🌴 ~ $ wnghub set-config exclude_repos "airflow,PyGithub" # Pass comma separated values for lists

🌴🌴🌴 ~ $ wnghub reset-config exclude_repos # Reset config to default value
```

### Setting up dev environment:
- Prerequisite: Have Python 3.7+ installed
- Clone repo
- Create virtual environment by running the following from the root of the repo: `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate`
- Install package by doing the following: `pip3 install -e .` from root of repo
- Install dev and testing requirements: `pip3 install -r dev-requirements.txt`
- Run `pytest` and ensure all tests are passing
- Install pre-commit: `pre-commit install`
- If everything looks good, you should be good to go
- To exit virtual environment, run `deactivate`. When you want to enter virtual environment again, navigate to root of repo and repeat the same command from above: `source venv/bin/activate`

### Code formatting:
- Should be done with [black](https://github.com/psf/black)

### Linting:
- Should be done with [flake8](https://github.com/PyCQA/flake8)
- KNOWN ISSUE: certain files are not yet passing flake8 checks. There is a Github issue re: this

### Testing:
- Done with [pytest](https://docs.pytest.org/en/stable/)
