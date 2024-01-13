"""
This module contains all the logic related to the answer entity
"""

from typing import Protocol


class QuizAnswerBase(Protocol):
    """
    This class represents the answer of the quiz

    Attributes:
        __text: the text of the answer
        __is_correct: boolean value that indicates if the answer is correct
    """

    __text: str
    __is_correct: bool

    @property
    def text(self) -> str:
        """
        This method returns the text of the answer
        """
        ...

    @property
    def is_correct(self) -> bool:
        """
        This method returns True if the answer is correct
        """
        ...


class QuizAnswer(QuizAnswerBase):
    """
    This class represents the answer of the quiz
    """

    def __init__(self, text: str, is_correct: bool):
        self.__text = text
        self.__is_correct = is_correct

    @property
    def text(self) -> str:
        """
        This method returns the text of the answer
        """
        return self.__text

    @property
    def is_correct(self) -> bool:
        """
        This method returns True if the answer is correct
        """
        return self.__is_correct

    def __str__(self):
        return f"Answer: {self.__text}"

    def __repr__(self):
        return f"Answer: {self.__text}"
