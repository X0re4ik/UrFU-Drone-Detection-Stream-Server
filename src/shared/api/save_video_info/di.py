from src.shared.libs.s3 import S3AdapterFactory
from src.shared.configs import PROJECT_SETTINGS

from .service import SaveVideoInfoAPI


class SaveVideoInfoAPIFactory:
    
    @staticmethod
    def create():
        _s3_config = PROJECT_SETTINGS.s3
        return SaveVideoInfoAPI(
            S3AdapterFactory.create(
                _s3_config.host,
                _s3_config.port,
                _s3_config.aws_access_key,
                _s3_config.aws_secret_key,
                _s3_config.use_ssl,
            ),
            _s3_config.bucket,
        )