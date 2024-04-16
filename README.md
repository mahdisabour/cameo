# CAME
The repository includes CAMEO backend application.

# Setup
The code is run with docker-compose.

## Development Environment
OS: Ubuntu 22.04.3 LTS

Python: CPython 3.11.5

# Backend Run
The code is executed with docker-compose in 3 modes:

```sh
docker-compose -f deployment/docker-compose.yml --env-file template.env up
```

## Tear Down
The setup could be stopped with docker-compose cli. For example:
```sh
docker-compose -f deployment/docker-compose.yml --env-file template.env down
```