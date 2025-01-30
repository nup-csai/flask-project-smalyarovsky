[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/d2zEkl7e)
# Food Tracker

## Solution for tracking your meals and snacks and calculating daily spending on food and daily calorie intake

Allows to input your meals and snacks with their data. Idea behind separation of snacks and meals is to help you track how much are you snacking during the day and help you transform you dietary habits to be healthier.

## Setup

The project is built with Docker. 
```bash
docker build . --file Dockerfile -t app
docker run -d -p 8080:8080 --name my_app_container -t app
```

## Requirements

Requires flask, flask-login, flask_sqlalchemy, requests, werkzeug, pytest (for testing, not necessary), 
## Features

Basic features:
1. Authorization system. Allows to login with different credentials for several people to use the app at the same time.
2. Inputting meals with price and nutritional values
3. Viewing statistics (daily spending on food, calorie intake)


## Git

The stable version of the app is stored in the master branch. unstable branch is for testing new features.

## CI/CD

GitHub actions is used for building and testing. Railway is used for CD. Link to the railway:
https://flask-project-smalyarovsky-production.up.railway.app/

## Logs

Logger Singleton class is used for logging. The logs can be found in app_[date].log file. 