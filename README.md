# Projectify Frontend

## Quickstart

```
cp .env.template .env
# Edit .env
```

## Running tests & linter

```
npm run check
npm run format
```

## Identifying slowly linted files

```
npm run format | sort --key=2 -h
```

## Installing the python tools

```
PIPENV_PIPFILE=Pipfile-tools pipenv sync --dev
```

And then

```
PIPENV_PIPFILE=Pipfile-tools pipenv run bin/rename_component.py
```

How to test

```
PIPENV_PIPFILE=Pipfile-tools pipenv run flake8
PIPENV_PIPFILE=Pipfile-tools pipenv run mypy
```

## Creating a new component

This will create a component and story file for you automatically.

```
bin/new_component path/within/src NameOfComponent
```
