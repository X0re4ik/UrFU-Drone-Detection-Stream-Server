from .service import RTSPStream

from src.shared.api.save_video_info import save_video_info_api


class RTSPStreamFactory:

    @staticmethod
    def create_from_rtmp_url(url: str):
        return RTSPStream(url)

    @staticmethod
    def create_from_s3(video_name: str):
        path_to_video = save_video_info_api.get_row_video_path(video_name)
        return RTSPStream(path_to_video)

    @staticmethod
    def create_from_md4(path_to_file: str):
        return RTSPStream(path_to_file)
