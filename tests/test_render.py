from bs4 import BeautifulSoup
from boto3.session import Session
import os
from pathlib import Path

from shares3.render import generate_sharing_html

PATH_PROJECT_HOME = Path(os.path.dirname(__name__)).parent


class TestRender:
    def test__generate_sharing_html(self):
        session = Session(profile_name="private-photo")
        html = generate_sharing_html(
            session=session,
            bucket="jyamane-photo-storage",
            prefix="test-shares3/testdir1/",
            expiration=15,
        )
        soup = BeautifulSoup(html, "html.parser")
        assert str(soup.find("title")) == "<title>testdir1</title>"

    def test__save_html(self):
        session = Session(profile_name="private-photo")
        html = generate_sharing_html(
            session=session,
            bucket="jyamane-photo-storage",
            prefix="test-shares3/testdir1/",
            expiration=15,
        )
        with open(PATH_PROJECT_HOME / "html" / "testdir1.html", "w") as fp:
            fp.write(html)
