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
