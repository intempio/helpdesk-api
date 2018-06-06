# biogen-helpdesk-api

[![Build Status](https://travis-ci.org/rustanacexd/biogen-helpdesk-api.svg?branch=master)](https://travis-ci.org/rustanacexd/biogen-helpdesk-api)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

todo. Check out the project's [documentation](http://rustanacexd.github.io/biogen-helpdesk-api/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  
- [Travis CLI](http://blog.travis-ci.com/2013-01-14-new-client/)
- [Heroku Toolbelt](https://toolbelt.heroku.com/)

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Continuous Deployment

Deployment is automated via Travis. When builds pass on the master or qa branch, Travis will deploy that branch to Heroku. Follow these steps to enable this feature.

Initialize the production server:

```
heroku create biogen_helpdesk-api-prod --remote prod && \
    heroku addons:create newrelic:wayne --app biogen_helpdesk_api-prod && \
    heroku addons:create heroku-postgresql:hobby-dev --app biogen_helpdesk_api-prod && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="biogen_helpdesk_api-prod" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="biogen_helpdesk_api.config" \
        --app biogen-helpdes-api-prod
```

Initialize the qa server:

```
heroku create biogen-helpdesk_api-qa --remote qa && \
    heroku addons:create newrelic:wayne --app biogen_helpdesk_api-qa && \
    heroku addons:create heroku-postgresql:hobby-dev --app biogen_helpdesk_api-qa && \
    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` \
        DJANGO_AWS_ACCESS_KEY_ID="Add your id" \
        DJANGO_AWS_SECRET_ACCESS_KEY="Add your key" \
        DJANGO_AWS_STORAGE_BUCKET_NAME="biogen_helpdesk_api-qa" \
        DJANGO_CONFIGURATION="Production" \
        DJANGO_SETTINGS_MODULE="biogen_helpdesk_api.config" \
        --app biogen_helpdesk_api-qa
```

Securely add your Heroku credentials to Travis so that it can automatically deploy your changes:

```bash
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
```

Commit your changes and push to master and qa to trigger your first deploys:

```bash
git commit -a -m "ci(travis): add Heroku credentials" && \
git push origin master:qa && \
git push origin master
```

You're now ready to continuously ship! ✨ 💅 🛳
