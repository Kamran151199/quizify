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

## Schema of CSV files

### Questions

- The questions csv file should have the following columns:
    - `question`: The question to be asked
    - `answer`: The correct answer to the question
    - `options`: The options separated by `;` (semi-colon)
    - `level`: Any meta data that you want to show to the user after the question has been answered

### Score Penalty

- The score penalty csv file should have the following columns:
    - `level`: The level of the question
    - `penalty`: The penalty to be applied to the score if the question is answered incorrectly

### Example CSV files

- [questions.csv](https://github.com/Kamran151199/quizify/blob/main/seeds/quiz_questions.csv)
- [score_penalty_config.csv](https://github.com/Kamran151199/quizify/blob/main/seeds/score_penalty.csv)

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