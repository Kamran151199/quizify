"""
This module contains the logic related to the quiz
"""

import abc
import csv
from pprint import pprint
from typing import Protocol

from quizify.check import QuizCheckerBase
from quizify.presenter import QuizPresenterBase
from quizify.question import QuizQuestionBase, QuizQuestion


class QuizBase(Protocol):
    """
    This class represents the quiz

    Attributes:
        _questions_path: the path to the questions.csv file
        __questions: the questions of the quiz
        checker: the checker of the quiz
        presenter: the presenter of the quiz
    """

    _questions_path: str = "quiz_questions.csv"
    __questions: list[QuizQuestionBase]
    checker: QuizCheckerBase
    presenter: QuizPresenterBase

    @abc.abstractmethod
    def run(self) -> None:
        """
        This method starts the quiz
        """
        ...

    @abc.abstractmethod
    def prepare(self) -> None:
        """
        This method prepares the quiz
        """
        ...

    @abc.abstractmethod
    def show_score(self, with_meta: bool) -> None:
        """
        This method shows the score of the quiz

        :param with_meta: boolean value that indicates if the meta data
        of the quiz should be shown
        """
        ...


class Quiz(QuizBase):
    """
    This class represents the quiz
    """

    def __init__(
            self,
            questions_path: str,
            checker: QuizCheckerBase,
            presenter: QuizPresenterBase
    ):
        """
        This method initializes the quiz

        :param questions_path: the path to the questions.csv file
        :param checker: the entity responsible for checking the quiz
        :param presenter: the entity responsible for presenting the quiz (interacting with the user)
        """
        self.__questions = []
        self._questions_path = questions_path
        self.checker = checker
        self.presenter = presenter

    def prepare(self) -> None:
        """
        Reads the questions from the questions.csv file
        :return: the questions
        """
        with open(self._questions_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                question_text, answer, options, level = row
                self.__questions.append(QuizQuestion(
                    text=question_text,
                    answer=answer,
                    options=options.split(';'),
                    level=level
                )
                )
        self.presenter.set_questions(self.__questions)

    def show_score(self, with_meta: bool) -> None:
        """
        This method shows the score of the quiz

        :param with_meta: boolean value that indicates if the meta data
        of the quiz should be shown
        """
        score = 0.0
        for question in self.__questions:
            score += self.checker.score(question)
        print(f"Your score is: {score}")

        if with_meta:
            presenter_meta = self.presenter.metadata
            checker_meta = self.checker.metadata
            self_metadata = self.metadata
            metadata = {
                **presenter_meta,
                **checker_meta,
                **self_metadata
            }
            pprint(metadata)

    def run(self) -> None:
        """
        This method starts the quiz
        """
        self.prepare()
        self.presenter.present()

    @property
    def metadata(self):
        return {
            "max_score": self.checker.calculate_max_score(self.__questions),
            "answered_questions": {
                question.text: getattr(question.accepted_answer, 'text', None)
                for question in self.__questions
                if question.accepted_answer is not None
            },
            "ignored_questions": {
                question.text: getattr(question.accepted_answer, 'text', None)
                for question in self.__questions
                if question.accepted_answer is None
            },
        }
