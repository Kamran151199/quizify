"""
This module contains the logic related to the check of the quiz
"""

import abc
import csv
from typing import Protocol

from quizify.question import QuizQuestionBase, QuizDifficultyLevelEnum


class QuizCheckerBase(Protocol):
    """
    This class represents the checker/assessor of the quiz
    """

    level_score_mapper: dict[QuizDifficultyLevelEnum, float]

    @abc.abstractmethod
    def score(
            self,
            question: QuizQuestionBase
    ) -> float:
        """
        This method checks the quiz
        """
        ...

    @abc.abstractmethod
    def calculate_max_score(self, questions: list[QuizQuestionBase]) -> float:
        """
        This method calculates the max score of the quiz
        """
        ...

    @property
    def metadata(self) -> dict:
        """
        This method returns the meta data of the checker
        """
        ...


class QuizChecker(QuizCheckerBase):
    """
    This class represents the checker/assessor of the quiz
    """

    def __init__(self, config_path: str):
        self._read_config(config_path)

    def score(self, question: QuizQuestionBase) -> float:
        """
        This method checks the quiz
        """

        score = self.level_score_penalty_mapper.get(
            question.level, {}).get('score', 1.0)
        penalty = self.level_score_penalty_mapper.get(
            question.level, {}).get('penalty', 0.5)

        if question.accepted_answer is None:
            return 0.0

        if question.accepted_answer.is_correct:
            return score

        return -penalty

    def _read_config(self, config_path: str) -> None:
        """
        This method reads the config file
        """

        self.level_score_penalty_mapper = {}

        with open(config_path) as config_file:
            reader = csv.reader(config_file)
            next(reader)

            for row in reader:
                level, score, penalty = row
                level_enum = getattr(QuizDifficultyLevelEnum, level.upper(), None)
                if level_enum is not None:
                    self.level_score_penalty_mapper[level_enum] = {
                        'score': float(score),
                        'penalty': float(penalty)
                    }

    @property
    def metadata(self) -> dict:
        """
        This method returns the meta data of the checker
        """
        return {
            'level_score_penalty_mapper': self.level_score_penalty_mapper
        }

    def calculate_max_score(self, questions: list[QuizQuestionBase]) -> float:
        """
        This method calculates the max score of the quiz
        """
        max_score = 0.0
        for question in questions:
            max_score += self.level_score_penalty_mapper.get(
                question.level, {}).get('score', 1.0)
        return max_score
