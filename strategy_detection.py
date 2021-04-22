from abc import ABCMeta, abstractmethod

class IStrategy_Detection(metaclass=ABCMeta):
    """Represent an strategy of error detections
    """
    @abstractmethod
    def check(self, frame):
        """Check if a frame was send using this strategy
        Return a boolean

        Args:
            frame (str): Is an string representation of a frame
        """
        pass
    
    @abstractmethod
    def apply(self, data):
        """Apply a strategy detection over data

        Args:
            data (str): Data to send on a frame
        """
        pass

   