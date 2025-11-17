"""
Tools that learn decision tree classifier
"""


# typing


from typing import Optional, Self


# libs


import os.path
from sklearn.tree import DecisionTreeClassifier as Model
from numpy import ndarray
from joblib import dump, load

from ..util import MachineLearningModel, Display
from .config import ModelConfig


""" Learning decision tree classifier tools
"""


""" Decision tree regressor object """


class DecisionTreeClassifier(MachineLearningModel):
    """
    Decision tree classifier model class.
    """

    """ model config """

    __config: type[ModelConfig] = ModelConfig
    @property
    def config(self) -> type[ModelConfig]: return self.__config

    """ model property """

    @property
    def model(self) -> Model: return self.get_model()

    """ Initialize"""

    def __init__(
            self,
            config: type[ModelConfig] = __config,
            model = None
    ) -> None:
        """
        Initialize and assign decision tree classifier object.
        :param config: Configuration that initialize decision tree classifier model.
        :param model: Initial model to initialize decision tree classifier model.
        """

        """ Initialize the model """

        if model is None:
            model = Model(
                max_depth=config.max_depth,
                random_state=config.random_state
            )
            ...

        MachineLearningModel.__init__(self, model)
        return

    """ Learning decision tree classifier model """

    @Display.fit_decorator
    def fit(
            self,
            X_train: ndarray,
            y_train: ndarray,
    ) -> None:
        """
        Fit decision tree classifier model.
        :param X_train:
        :param y_train:
        :return: None
        """
        import time
        self.model.fit(X_train, y_train)
        return

    def save(self, path: str) -> Optional[str]:
        """
        Save decision tree classifier model.
        :param path: Path to save model.
        :return: Saved file path.
        """
        print(f"Saving model to {path}")
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
            ...
        dump(self.model, path)
        print(f"Successfully saved model to {path}")
        return path

    @classmethod
    def load(cls, path: str) -> Self:
        """
        Load decision tree classifier model.
        :param path: Path to load model.
        :return: Self
        """
        print(f"Loading model from {path}")
        ins = cls(model=load(path))
        print(f"Successfully loaded model from {path}")
        return ins

    ...
