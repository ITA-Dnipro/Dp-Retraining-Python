# Retraining project
[![Status](https://github.com/ITA-Dnipro/Dp-Retraining-Python/actions/workflows/dev_checks.yml/badge.svg)](https://github.com/ITA-Dnipro/Dp-Retraining-Python/actions/workflows/dev_checks.yml)

A retraining project to get familiar with various technologies.
## How to set up and run
### How to get project:
```
git clone https://github.com/ITA-Dnipro/Dp-Retraining-Python.git
```
## How to set up .env files:
### Manual setup
You can manually create and put env variables inside .env file in each folder where .env.example file is present.
### Make file setup
Use command to setup .env files with default development variables
```
make env_setup
```
## How to run project
### Make file docker commands
1. Run command to build and start docker-compose
```
make up
```
2. Run command to stop docker-compose
```
make down
```
3. To remove docker components use commands:
- To remove all docker containers
```
make remove_all_containers
```
- To remove all docker images
```
make remove_all_images
```
- To remove all docker volumes
```
make remove_all_volumes
```
- (!) To remove all docker containers AND images AND volumes (!)
```
make remove_everything
```
### Manual docker commands
1. Run command to build and start docker-compose
```
docker-compose -f ${PWD}/docker-compose.yml up --build -d
```
2. Run command to start already created docker-compose
```
docker-compose -f ${PWD}/docker-compose.yml -d start
```
3. Run command to stop docker-compose
```
docker-compose -f ${PWD}/docker-compose.yml down
```
## How to run tests and create coverage reports
1. Use command to run all tests
```
make run_tests
```
2. Use command to create .coverage file
```
make coverage
```
3. Use command to create folder with html report
```
make coverage_html_report
```
