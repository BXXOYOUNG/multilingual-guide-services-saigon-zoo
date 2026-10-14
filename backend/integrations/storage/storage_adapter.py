from abc import ABC, abstractmethod


class StorageAdapter(ABC):
    """
    Abstract interface for file and object storage (e.g., local storage, S3).
    Follows Technology Baseline 3 and Rule 18 (Must keep external services behind adapters).
    """

    @abstractmethod
    def get_public_url(self, file_path: str) -> str:
        """
        Returns a publicly accessible or downloadable URL for a given relative or absolute file path.
        """
        pass

    @abstractmethod
    async def file_exists(self, file_path: str) -> bool:
        """
        Checks whether a file exists at the given path.
        """
        pass


class LocalStorageAdapter(StorageAdapter):
    """
    Storage adapter that resolves relative file paths to base URL or media prefix.
    """

    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url.rstrip("/")

    def get_public_url(self, file_path: str) -> str:
        if file_path.startswith("http://") or file_path.startswith("https://"):
            return file_path
        clean_path = file_path.lstrip("/")
        return f"{self.base_url}/{clean_path}" if self.base_url else f"/{clean_path}"

    async def file_exists(self, file_path: str) -> bool:
        return True

