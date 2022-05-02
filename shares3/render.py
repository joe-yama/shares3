from dataclasses import asdict
import os
from pathlib import Path

from boto3.session import Session
from jinja2 import Environment, FileSystemLoader

from shares3.presigner import Presigner, PresignedS3Object

PATH_PROJECT_HOME = Path(os.path.dirname(__name__)).parent
PATH_TEMPLETES = PATH_PROJECT_HOME / "templetes"


def generate_sharing_html(
    session: Session, bucket: str, prefix: str, expiration: int
) -> str:
    presiner = Presigner(session=session)
    presignees = presiner.presign(
        bucket=bucket,
        prefix=prefix,
        expiration=expiration,
    )
    title = prefix.strip("/ ").split("/")[-1]
    sharing_objects = [asdict(presignee) for presignee in presignees]
    params = {"title": title, "sharing_objects": sharing_objects}

    env = Environment(loader=FileSystemLoader(str(PATH_TEMPLETES)), trim_blocks=True)
    template = env.get_template("template.jinja")
    return template.render(params)
