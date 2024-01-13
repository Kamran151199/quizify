"""
The entry point of the application
"""

import argparse

from quizify.check import QuizChecker
from quizify.presenter import QuizPresenter
from quizify.quiz import Quiz


def main():
    """
    The entry point of the application
    """

    parser = argparse.ArgumentParser(description="Quizify")

    parser.add_argument(
        "--questions",
        type=str,
        help="Path to the questions CSV file",
        default="./seeds/quiz_questions.csv"
    )
    parser.add_argument(
        "--score-penalty",
        type=str,
        help="Path to the score/penalty CSV file",
        default="./seeds/score_penalty.csv"
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help="Shuffle the questions",
        default=True
    )

    parser.add_argument(
        "--show-meta",
        action="store_true",
        help="Show the meta data of the quiz",
        default=False
    )

    args = parser.parse_args()

    quiz_checker = QuizChecker(args.score_penalty)
    quiz_presenter = QuizPresenter(shuffle=args.shuffle)
    quiz = Quiz(
        questions_path=args.questions,
        checker=quiz_checker,
        presenter=quiz_presenter
    )
    quiz.run()
    quiz.show_score(with_meta=args.show_meta)


if __name__ == "__main__":
    main()
