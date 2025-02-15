from gpt_engineer.core.base_version_manager import BaseVersionManager
from gpt_engineer.core.code import Code
from gpt_engineer.core.default.on_disk_repository import OnDiskRepository


class GitVersionManager(BaseVersionManager):
    """
    Manages versions of code using Git as the version control system.

    This class is responsible for creating snapshots of the code, which typically involves
    saving the code to a file and committing it to a Git repository. The snapshot method
    returns a unique hash that can be used to identify the version of the code.

    Attributes:
        path (str): The file system path where the Git repository is located.
    """

    def __init__(self, path: str):
        self.path = path

    def snapshot(self, code: Code) -> str:
        workspace = OnDiskRepository(self.path)
        for file_name, file_content in code.items():
            workspace[file_name] = file_content
        # Typically save to file and/or git and return a hash

        # Todo: Implement push to git!
        return ""
