from .service import VideoWriterService


class VideoWriterServiceFactory:

    @staticmethod
    def create(task_id: str, fps: int, size: tuple[int, int]):
        return VideoWriterService(
            task_id,
            fps,
            size[0],
            size[1],
        )
