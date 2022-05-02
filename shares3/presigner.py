from dataclasses import dataclass
from typing import List

from boto3.session import Session

from shares3.utils import human_readable_size


@dataclass
class PresignedS3Object:
    key: str
    size: str
    presigned_url: str
    bucket_name: str
    expiration: int


class Presigner:
    def __init__(self, session: Session) -> None:
        self._session = session
        # self._session = Session(profile_name=profile) if profile else Session()
        self._s3resource = self._session.resource("s3")
        self._s3client = self._session.client("s3")

    def presign(
        self, bucket: str, prefix: str, expiration: int
    ) -> List[PresignedS3Object]:
        results: List[PresignedS3Object] = []
        objs = self._s3resource.Bucket(bucket).objects.filter(Prefix=prefix)
        for obj in objs:
            url = self._s3client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": obj.bucket_name, "Key": obj.key},
                ExpiresIn=expiration,
                HttpMethod="GET",
            )
            results.append(
                PresignedS3Object(
                    key=obj.key,
                    size=human_readable_size(obj.size, decimal_places=1),
                    presigned_url=url,
                    bucket_name=bucket,
                    expiration=expiration,
                )
            )
        return results
