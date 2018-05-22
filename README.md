[![License: MIT](https://img.shields.io/github/license/vintasoftware/django-react-boilerplate.svg)](LICENSE.txt)

# Github Monitor

## About
A [Django 1.11](https://www.djangoproject.com/) project with lots of state of the art libraries and tools like:
- [React](https://facebook.github.io/react/), for building interactive UIs
- [django-js-reverse](https://github.com/ierror/django-js-reverse), for generating URLs on JS
- [Bootstrap 4](https://v4-alpha.getbootstrap.com/), for responsive styling
- [Webpack](https://webpack.js.org/), for bundling static assets
- [Celery](http://www.celeryproject.org/), for background worker tasks
- [WhiteNoise](http://whitenoise.evans.io/en/stable/) with [brotlipy](https://github.com/python-hyper/brotlipy), for efficient static files serving
- [prospector](https://prospector.landscape.io/en/master/) and [ESLint](https://eslint.org/) with [pre-commit](http://pre-commit.com/) for automated quality assurance (does not replace proper testing!)

For continuous integration, a [CircleCI](https://circleci.com/) configuration `circle.yml` is included.

Also, includes a Heroku `app.json` and a working Django `production.py` settings, enabling easy deployments with ['Deploy to Heroku' button](https://devcenter.heroku.com/articles/heroku-button). Those Heroku plugins are included in `app.json`:
- PostgreSQL, for DB
- Redis, for Celery
- Sendgrid, for e-mail sending
- Papertrail, for logs and platform errors alerts (must set them manually)


## Running
### Setup
- On project root, do the following:
- Create a copy of ``ghmonitor/settings/local.py.example``:  
  `cp ghmonitor/settings/local.py.example ghmonitor/settings/local.py` (remembering you should replace `ghmonitor` with your project's name!).
- Create a copy of ``.env.example``:  
  `cp .env.example .env`
- If you get an "there's no module named Django" error, install it through `pip install django<2` and try the step above again.
- Run the migrations:  
  `python manage.py migrate`

### Tools
- Setup [editorconfig](http://editorconfig.org/), [prospector](https://prospector.landscape.io/en/master/) and [ESLint](http://eslint.org/) in the text editor you will use to develop.

### Running the project
- Open a command line window and go to the project's directory.
- `pipenv install --dev`
- `npm install`
- `npm run start`
- Open another command line window and go to the project's directory.
- `pipenv shell`
- `python manage.py runserver`

### Testing
`make test`

Will run django tests using `--keepdb` and `--parallel`. You may pass a path to the desired test module in the make command. E.g.:

`make test someapp.tests.test_views`

### Adding new pypi libs
Just run `pipenv install LIB_NAME_ON_PYPI` and then `pipenv lock` to lock the version in Pipfile.lock file

## Linting
- Manually with `prospector` and `npm run lint` on project root.
- During development with an editor compatible with prospector and ESLint.

## Pre-commit hooks
- Run `pre-commit install` to enable the hook into your git repo. The hook will run automatically for each commit.
- Run `git commit -m "Your message" -n` to skip the hook if you need.

## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Credits
This project, was created using [django-react-boilerplate](https://github.com/vintasoftware/django-react-boilerplate) by [Vinta](https://www.vinta.com.br).

Copyright (c) 2018 Vinta Serviços e Soluções Tecnológicas Ltda.
[MIT License](LICENSE.txt)
