from .video_service_interface import IVideoService

class LocalVideoService(IVideoService):

    def get_video_data(self, video_id: str):
        # Información simulada para cuando no queremos usar la API real
        return {
            "snippet": {
                "title": "Video de Ejemplo Local",
                "description": "Este es un video cargado localmente sin usar API.",
                "thumbnails": {
                    "high": {"url": "https://i.ytimg.com/vi/Owj9PaLnB14/hqdefault.jpg"}
                }
            }
        }
