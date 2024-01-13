"""
This module contains all the logic related to the question entity
"""

import abc
from enum import Enum
from typing import Protocol

from quizify.answer import QuizAnswerBase, QuizAnswer


class QuizDifficultyLevelEnum(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuizQuestionBase(Protocol):
    """
    This class represents the question of the quiz

    Attributes:
        __text: the text of the question
        __options: the options of the question
        __level: the difficulty level of the question
        __answer: the correct answer of the question
        __accepted_answer: the answer/response given by the user
    """

    __text: str
    __options: list[str]
    __level: str
    __answer: str
    __accepted_answer: QuizAnswerBase | None

    @abc.abstractmethod
    def accept_answer(self, user_answer: str) -> None:
        """
        This method accepts the user answer
        """
        ...

    @property
    def options(self) -> list[QuizAnswerBase]:
        """
        This method returns the options of the question.
        Meant to be a property of the question
        """
        ...

    @property
    def text(self) -> str:
        """
        This method returns the text of the question
        Meant to be a property of the question
        """
        ...

    @property
    def accepted_answer(self) -> QuizAnswerBase:
        """
        This method returns the accepted answer
        """
        ...

    @property
    def level(self) -> QuizDifficultyLevelEnum:
        """
        This method returns the difficulty level of the question
        """
        ...


class QuizQuestion(QuizQuestionBase):
    """
    This class represents the question of the quiz
    """

    def __init__(
            self,
            text: str,
            options: list[str],
            level: str,
            answer: str
    ):
        self.__text = text
        self.__answer = answer
        self.__options = options
        self.__level = level
        self.__accepted_answer = None

        self._validate()

    def _validate(self) -> None:
        """
        This method validates the question
        """
        if not all([self.__text, self.__options, self.__level, self.__answer]):
            raise ValueError("Invalid question")

        if self.__level not in [level.value for level in QuizDifficultyLevelEnum]:
            raise ValueError(f"Invalid level: {self.__level}")

        if self.__answer not in self.__options:
            raise ValueError("Invalid answer")

    def accept_answer(self, user_answer: str) -> None:
        """
        This method accepts the user answer
        """

        if self.accepted_answer is not None:
            raise ValueError("The answer was already accepted")

        answer = [option for option in self.options if option.text == user_answer]

        if len(answer) == 0:
            raise ValueError("The answer is not in the options")

        self.__accepted_answer = answer[0]

    @property
    def options(self) -> list[QuizAnswerBase]:
        """
        This method returns the options of the question.
        Meant to be a property of the question
        """
        return [self.__options_to_answer_obj(option) for option in self.__options]

    @property
    def text(self) -> str:
        """
        This method returns the text of the question
        Meant to be a property of the question
        """
        return self.__text

    @property
    def accepted_answer(self) -> QuizAnswerBase:
        """
        This method returns the accepted answer
        """
        return self.__accepted_answer

    @property
    def level(self) -> QuizDifficultyLevelEnum:
        """
        This method returns the difficulty level of the question
        """
        return QuizDifficultyLevelEnum(self.__level)

    def __options_to_answer_obj(self, text: str) -> QuizAnswerBase:
        """
        This method converts a string to an answer object
        """
        return QuizAnswer(text=text, is_correct=text == self.__answer)

    def __str__(self):
        return f"Question: {self.__text}, Level: {self.level.value}"

    def __repr__(self):
        return f"Question: {self.__text}, Level: {self.level.value}"
