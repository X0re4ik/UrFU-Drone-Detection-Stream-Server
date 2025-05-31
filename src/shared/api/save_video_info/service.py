import io
from src.shared.libs.s3 import S3AdapterFactory, S3Adapter


class SaveVideoInfoAPI:

    def __init__(self, s3_adapter: S3Adapter, bucket: str):
        self._s3_adapter = s3_adapter
        self._bucket = bucket

    def save_row_video(self, file_name: str, video: io.BytesIO) -> None:
        self._s3_adapter.upload_file(
            self._bucket, f"rows/{file_name}", video.getvalue()
        )

    def save_processed_video(self, file_name: str, video: io.BytesIO) -> None:
        self._s3_adapter.upload_file(
            self._bucket, f"processed/{file_name}", video.getvalue()
        )

    def get_row_video_path(self, file_name: str) -> str:
        path_to_file = self._s3_adapter.download_to_tmp(
            self._bucket,
            f"rows/{file_name}",
        )
        return path_to_file

    def get_processed_video(self, file_name: str) -> io.BytesIO:
        _, video_file = self._s3_adapter.download_file_bytes(
            self._bucket, f"processed/{file_name}"
        )

        return io.BytesIO(video_file)

    def get_row_video(self, file_name: str) -> io.BytesIO:
        _, video_file = self._s3_adapter.download_file_bytes(
            self._bucket, f"rows/{file_name}"
        )

        return io.BytesIO(video_file)

    def save_report(self, file_name: str, report: io.BytesIO) -> None:
        self._s3_adapter.upload_file(
            self._bucket, f"report/{file_name}", report.getvalue()
        )

    def get_report(self, file_name: str) -> io.BytesIO:
        _, video_file = self._s3_adapter.download_file_bytes(
            self._bucket, f"report/{file_name}"
        )
        return io.BytesIO(video_file)
