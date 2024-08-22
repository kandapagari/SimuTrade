from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def generate_signals(self, df):
        raise NotImplementedError("Subclasses must implement this method")
