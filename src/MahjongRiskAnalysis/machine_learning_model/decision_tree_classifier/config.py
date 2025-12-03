"""
Config of decision tree classifier.
"""


# typing


# libs


from TenhouAPI.util.config import ConfigBase


""" Decision tree classifier configs
"""


class ModelConfig(ConfigBase):
    """
    Config that learn decision tree classifier.
    """

    max_depth: int = 15
    random_state: int = 0

    ...
