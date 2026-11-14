
from pathlib import Path


class FilesystemTools:

    MAX_FILE_SIZE = 1_000_000  # 1 MB
    MAX_SEARCH_RESULTS = 100

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()

        if not self.workspace_root.exists():
            raise ValueError("Workspace directory does not exist")

        if not self.workspace_root.is_dir():
            raise ValueError("Workspace root must be a directory")

    def _resolve_path(self, relative_path: str) -> Path:
        """
        Convert a repository-relative path into an absolute path.
        Prevent access outside the configured workspace.
        """

        if not relative_path:
            raise ValueError("Path cannot be empty")

        target = (self.workspace_root / relative_path).resolve()

        if not target.is_relative_to(self.workspace_root):
            raise ValueError("Access outside workspace is not allowed")

        return target

    def list_directory(self, path: str = "."):
        directory = self._resolve_path(path)

        if not directory.exists() or not directory.is_dir():
            raise ValueError("Directory does not exist")

        entries = []

        for item in sorted(directory.iterdir()):
            if item.name.startswith("."):
                continue

            entries.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file"
            })

        return {
            "path": path,
            "entries": entries[:200],
            "total_entries": len(entries)
        }

    def read_file(self, path: str):
        file_path = self._resolve_path(path)

        if not file_path.exists() or not file_path.is_file():
            raise ValueError("File does not exist")

        if file_path.stat().st_size > self.MAX_FILE_SIZE:
            raise ValueError("File exceeds the 1 MB read limit")

        content = file_path.read_text(encoding="utf-8")

        return {
            "path": path,
            "content": content
        }

    def search_code(self, query: str, path: str = "."):
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        search_root = self._resolve_path(path)

        if not search_root.exists():
            raise ValueError("Search path does not exist")

        ignored_directories = {
            ".git", ".venv", "__pycache__", "node_modules"
        }

        results = []

        if search_root.is_file():
            files = [search_root]
        elif search_root.is_dir():
            files = (
                file for file in search_root.rglob("*")
                if file.is_file()
                   and not any(
                part in ignored_directories
                for part in file.relative_to(search_root).parts
            )
                   and not any(
                part.startswith(".")
                for part in file.relative_to(search_root).parts
            )
            )
        else:
            raise ValueError("Invalid search path")

        for file_path in files:
            if file_path.stat().st_size > self.MAX_FILE_SIZE:
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            for line_number, line in enumerate(content.splitlines(), start=1):
                if query.lower() in line.lower():
                    results.append({
                        "file": str(file_path.relative_to(self.workspace_root)),
                        "line": line_number,
                        "content": line.strip()
                    })

                    if len(results) >= self.MAX_SEARCH_RESULTS:
                        return {
                            "query": query,
                            "matches": results,
                            "truncated": True
                        }

        return {
            "query": query,
            "matches": results,
            "truncated": False
        }

    def write_file(
            self,
            path: str,
            content: str,
            allow_overwrite: bool = False
    ):
        file_path = self._resolve_path(path)

        if len(content.encode("utf-8")) > self.MAX_FILE_SIZE:
            raise ValueError("Content exceeds the 1 MB write limit")

        if file_path.exists() and not allow_overwrite:
            raise ValueError(
                "File already exists. Explicit overwrite permission required."
            )

        if file_path.exists() and not file_path.is_file():
            raise ValueError("Target path is not a file")

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        return {
            "path": path,
            "status": "written",
            "bytes_written": len(content.encode("utf-8"))
        }
