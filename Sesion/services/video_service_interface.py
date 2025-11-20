from abc import ABC, abstractmethod

class IVideoService(ABC):

    @abstractmethod
    def get_video_data(self, video_id: str):
        """Retorna la información del video según su implementación."""
        pass
