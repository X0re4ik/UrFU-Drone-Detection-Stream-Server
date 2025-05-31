from .client import S3Adapter


class S3AdapterFactory:

    @staticmethod
    def create(
        host: str,
        port: int,
        aws_access_key: str,
        aws_secret_key: str,
        use_ssl: bool
    ):
        return S3Adapter(
            host,
            port,
            aws_access_key,
            aws_secret_key,
            use_ssl=use_ssl,
        ).initialize()
