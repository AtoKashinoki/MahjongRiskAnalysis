"""
Utility tools that lean machine learning models.
"""

# typing


from typing import (
    TypeVar, Union, Optional, Self
)

T = TypeVar('T')


# libs


from abc import ABC, abstractmethod
import functools
import time
from threading import Thread

from sklearn.base import ClassifierMixin, RegressorMixin


""" Machine learning model utility tools
"""


""" Machine learning model skeleton class """


class MachineLearningModel(ABC):
    """
    Skeleton class for machine learning models.\n
    We can create new machine learning model with this skeleton class.\n
    Required methods\n
    - model property method: Return model instance.
    - fit method: Fit machine learning model.
    Recommended methods\n
    - __init__ method: Assign machine learning model.
    """

    """ Initialize """

    def __init__(
            self,
            machine_learning_model: T
    ) -> None:
        """
        Assign machine learning model process.
        :param machine_learning_model: Machine learning model
        """
        self.__model: T = machine_learning_model
        return

    """ model """

    __model: Union[ClassifierMixin, RegressorMixin]

    def get_model(self):
        """
        Return machine learning model.
        :return: Machine learning model
        """
        return self.__model

    @property
    @abstractmethod
    def model(self) -> Union[ClassifierMixin, RegressorMixin]:
        """
        Return machine learning model.
        :return: Machine learning model
        """
        ...

    @abstractmethod
    def fit(self, *args, **kwargs) -> None:
        """
        Fit machine learning model.
        :return: None
        """
        ...

    @abstractmethod
    def save(self, path: str) -> Optional[str]:
        """
        Save machine learning model.
        :param path: Path to save model
        :return: Saved file path.
        """
        ...

    @classmethod
    @abstractmethod
    def load(cls, path: str) -> Self:
        """
        Load machine learning model.
        :param path: Path of model to load.
        :return: Self
        """
        ...

    ...


""" Display thread decorator and wrapper """


class DisplayWrapper(Thread):
    """
    Display for machine learning model processes in the console.
    """

    """ initialize tread """

    def __init__(
            self,
            thread_name: str,
    ) -> None:
        """
        Initialize tread.
        :param thread_name: Name of the thread.
        """
        Thread.__init__(
            self,
            name=thread_name,
        )
        self.__done = False
        return

    """ run method """

    @abstractmethod
    def main(self, *args, **kwargs) -> None:
        """ Display main """
        return

    """ Call run method """

    def run(self, *args, **kwargs) -> None:
        """ call wrapped method """

        while not self.__done:
            self.main(*args, **kwargs)
            continue
        print()

        return


    """ Stop calling method """

    def stop(self) -> None:
        """
        Stop self thread.
        :return: None
        """
        self.__done = True
        return

    ...


""" Display decorators """


class DisplayFit(DisplayWrapper):
    """
    Display for fitting machine learning model in the console.
    """

    @staticmethod
    def main(
            display_text: str = "Fitting machine learning model",
    ) -> None:
        """
        Display of fit process.
        :param display_text: Display text.
        :return: None
        """
        print(end="")
        for i in range(4):
            print("\r", display_text, "." * i, " "*(4-i), sep="", end="")
            time.sleep(0.5)
            continue
        return
    ...


class Display:
    """
    Display for machine learning model processes in the console.
    """

    """ fit """

    @staticmethod
    def fit_decorator(func):
        """
        Add display of fit process
        :param func: Fit method.
        :return: Wrapped method.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # start display process
            display = DisplayFit(func.__name__)
            display.start()

            try:

                result = func(*args, **kwargs)
                ...
            except Exception as e:
                display.stop()
                display.join()
                raise e

            # stop display process
            display.stop()
            display.join()

            return result

        return wrapper

    ...
