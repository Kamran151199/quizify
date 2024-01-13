"""
This module contains all the logic related to the presenter of the quiz
"""

import abc
import random
import time
from typing import Protocol

from quizify.question import QuizQuestionBase


class QuizPresenterBase(Protocol):
    """
    This class represents the presenter of the quiz
    """

    __skipped_questions: list[QuizQuestionBase]
    __questions_timer: dict[QuizQuestionBase, float]
    __questions: list[QuizQuestionBase]

    @abc.abstractmethod
    def set_questions(self, questions: list[QuizQuestionBase]) -> None:
        """
        This method sets the questions of the quiz
        """
        ...

    @abc.abstractmethod
    def present(self) -> None:
        """
        This method presents the quiz questions to the user
        and accepts the user answers
        """
        ...

    @abc.abstractmethod
    def present_question(self, question: QuizQuestionBase) -> None:
        """
        This method presents the question to the user
        and accepts the user answer
        """
        ...

    @abc.abstractmethod
    def skip_question(self, question: QuizQuestionBase) -> None:
        """
        This method skips the question
        """
        ...

    @abc.abstractmethod
    def shuffle_questions(self) -> None:
        """
        This method shuffles the questions of the quiz
        :return: the shuffled questions
        """
        ...

    @property
    def metadata(self) -> dict:
        """
        This method displays the metadata of the quiz
        """
        ...


class QuizPresenter(QuizPresenterBase):
    """
    This class represents the presenter of the quiz
    """

    def __init__(self, shuffle: bool = False):
        """
        This method initializes the presenter of the quiz

        :param shuffle: boolean value that indicates if the questions should be shuffled
        """
        self.__skipped_questions = []
        self.__questions_timer = {}
        self.__questions = []
        self.__shuffle = shuffle
        self.__start = None
        self.__end = None

    def set_questions(self, questions: list[QuizQuestionBase]) -> None:
        """
        This method sets the questions of the quiz
        """
        self.__questions = questions

        if self.__shuffle:
            self.shuffle_questions()

    def present_question(self, question: QuizQuestionBase) -> None:
        """
        This method presents the question to the user
        and accepts the user answer
        """

        if not self.__questions:
            raise ValueError("Questions not set")

        self.__questions_timer[question] = self.__questions_timer.get(question, 0.0)
        start = time.time()

        result = "\n"
        result += f"Question: {question.text}\n"

        for k, v in self.options_enumerated(question).items():
            result += f"{k}) {v}\n"

        print(result)
        choice = input("Your answer: ")

        # TODO: move this to a separate method (e.g. interpret_command)
        if choice == "!skip":
            self.skip_question(question)
            return

        if choice == "!ignore":
            self.__questions_timer[question] += time.time() - start
            return

        answer = self.options_enumerated(question).get(choice, None)

        try:
            if answer is None:
                raise ValueError
            question.accept_answer(answer)
        except ValueError:
            print("Invalid answer")
            self.__questions_timer[question] += time.time() - start
            return self.present_question(question)
        self.__questions_timer[question] += time.time() - start

    def skip_question(self, question: QuizQuestionBase) -> None:
        """
        This method skips the question
        """
        self.__skipped_questions.append(question)

    def present(self) -> None:
        """
        This method presents the quiz questions to the user
        and accepts the user answers
        """

        if self.__start is None:
            self.__start = time.time()

        for question in self.__questions:
            self.present_question(question)

        if self.__skipped_questions:
            print("Resuming skipped questions...")
            self.set_questions(self.__skipped_questions)
            self.__skipped_questions = []
            self.present()
        self.__end = time.time()

    def shuffle_questions(self) -> None:
        """
        This method shuffles the questions of the quiz
        :return: the shuffled questions
        """
        random.shuffle(self.__questions)

    @staticmethod
    def options_enumerated(question: QuizQuestionBase) -> dict[str, str]:
        result = {}
        for idx, option in enumerate(question.options):
            result[chr(ord('a') + idx)] = option.text
        return result

    @property
    def metadata(self) -> dict:
        """
        This method displays the metadata of the quiz
        """
        return {
            "time_per_question": self.__questions_timer,
            "total_time": self.__end - self.__start,
        }
