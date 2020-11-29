# wnghub

### 'what's new on github'

### How to use:
- Installation (only tested Python 3.7+): `pip3 install git+https://github.com/brighton1101/wnghub.git`
- Run it! `wnghub` for unread notifications, `wnghub -A` to include read notifications
- Note that currently, this will only show the five most recent for either option
- Still very much a WIP

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
