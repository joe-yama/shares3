import requests

from boto3.session import Session

from shares3.presigner import Presigner, PresignedS3Object


class TestPresigner:
    def test__init(self):
        session = Session()
        presiner = Presigner(session=session)

    def test__presign(self):
        session = Session(profile_name="private-photo")
        presiner = Presigner(session=session)
        presignees = presiner.presign(
            bucket="jyamane-photo-storage",
            prefix="test-shares3/testdir1/",
            expiration=15,
        )
        assert len(presignees) == 2
        actuals = ("testdata1\n", "testdata2\n")
        for presignee, actual in zip(presignees, actuals):
            response = requests.get(presignee.presigned_url)
            assert response.text == actual
