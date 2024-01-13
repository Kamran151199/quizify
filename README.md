# Quizify - A Quiz App

## Description

This is a cli quiz app that allows users to take a quiz and assess their knowledge on a particular topic.
It reads questions from csv files and presents them to the user. The user can then select an answer.
At the end of the quiz, the user is presented with their score.

## Requirements

- Python 3.10 or higher

## Installation

### Option 1

- Clone the repo:
  `git clone https://github.com/Kamran151199/quizify.git`
- Navigate to the project directory:
    - `cd quizify`
- Run `poetry install` to install dependencies
- Run `poetry run quizify` to start the app

### Option 2

- Install from PyPi:
    - `pip install quizify`
- Run `quizify` to start the app
- Run `quizify --help` to see available options

## Example Usage

- `quizify --help` to see available options
- `quizify --score-penalty=score_penalty_config.csv --questions=questions.csv` to start the app with custom config
  and questions.
- `quizify --score-penalty=score_penalty_config.csv --questions=questions.csv --shuffle` to start the app with custom
  config
  and questions and shuffle the questions.
- `quizify --score-penalty=score_penalty_config.csv --questions=questions.csv --shuffle --with-meta` to start the app
  with custom config
  and questions and shuffle the questions and show meta data.