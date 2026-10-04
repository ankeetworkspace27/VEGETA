import os
import shutil
import ctypes
import uuid
from ctypes import wintypes
from pathlib import Path


class FileManager:
    """Handles basic file and folder operations for VEGETA."""

    def expand_path(self, path):
        if not path:
            return None
        path = os.path.expandvars(os.path.expanduser(str(path).strip()))
        return os.path.abspath(path)

    def get_known_folder(self, folder_name):
        """Return the real Windows Known Folder path.

        This handles redirected folders such as Downloads/Pictures instead
        of assuming they are always directly under the user's home folder.
        """
        aliases = {
            "download": "downloads",
            "downloads": "downloads",
            "document": "documents",
            "documents": "documents",
            "desktop": "desktop",
            "picture": "pictures",
            "pictures": "pictures",
            "music": "music",
            "video": "videos",
            "videos": "videos",
        }

        name = str(folder_name).strip().lower()
        name = aliases.get(name, name)

        guids = {
            "downloads": "374DE290-123F-4565-9164-39C4925E467B",
            "documents": "FDD39AD0-238F-46AF-ADB4-6C85480369C7",
            "desktop": "B4BFCC3A-DB2C-424C-B029-7FE99A87C641",
            "pictures": "33E28130-4E1E-4676-835A-98395C3BC3BB",
            "music": "4BD8D571-6D19-48D3-BE97-422220080E43",
            "videos": "18989B1D-99B5-455B-841C-AB7C74E4DDFC",
        }

        fallback = {
            "downloads": os.path.expanduser("~/Downloads"),
            "documents": os.path.expanduser("~/Documents"),
            "desktop": os.path.expanduser("~/Desktop"),
            "pictures": os.path.expanduser("~/Pictures"),
            "music": os.path.expanduser("~/Music"),
            "videos": os.path.expanduser("~/Videos"),
        }

        if name not in guids:
            return None

        # Windows Known Folder API. Fall back gracefully if unavailable.
        try:
            class GUID(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", wintypes.BYTE * 8),
                ]

            guid = GUID.from_buffer_copy(uuid.UUID(guids[name]).bytes_le)
            path_ptr = ctypes.c_wchar_p()

            result = ctypes.windll.shell32.SHGetKnownFolderPath(
                ctypes.byref(guid),
                0,
                None,
                ctypes.byref(path_ptr),
            )

            if result == 0 and path_ptr.value:
                path = path_ptr.value
                ctypes.windll.ole32.CoTaskMemFree(path_ptr)
                return path
        except Exception as error:
            print(f"VEGETA FILE: Known folder lookup warning -> {error}")

        return fallback[name]

    def get_special_folder(self, folder_name):
        return self.get_known_folder(folder_name)

    def open_path(self, path):
        path = self.expand_path(path)
        if not path or not os.path.exists(path):
            print(f"VEGETA FILE: Path not found -> {path}")
            return False
        try:
            os.startfile(path)
            print(f"VEGETA FILE: Opened -> {path}")
            return True
        except Exception as error:
            print(f"VEGETA FILE: Open failed -> {error}")
            return False

    def create_folder(self, path):
        path = self.expand_path(path)
        if not path:
            return False
        try:
            os.makedirs(path, exist_ok=True)
            print(f"VEGETA FILE: Folder created -> {path}")
            return True
        except Exception as error:
            print(f"VEGETA FILE: Folder creation failed -> {error}")
            return False

    def _default_search_roots(self):
        home = Path.home()
        names = ("Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music")
        roots = []
        for name in names:
            path = home / name
            if path.exists() and path.is_dir():
                roots.append(str(path))
        # Keep the home folder as a final fallback, but only if the common
        # folders produced no useful results.
        return roots

    def _search_root(self, root, name, results):
        try:
            for current_root, directories, files in os.walk(root, topdown=True):
                # Never descend into hidden/system/cache-heavy profile folders.
                directories[:] = [
                    d for d in directories
                    if d.lower() not in {"appdata", "$recycle.bin"}
                    and not d.startswith(".")
                ]
                for item in directories + files:
                    if name in item.lower():
                        results.append(os.path.join(current_root, item))
                        if len(results) >= 100:
                            return
        except (PermissionError, OSError) as error:
            print(f"VEGETA FILE: Search warning -> {error}")

    def find(self, name, search_directory=None):
        if not name:
            return []
        name = str(name).strip().lower()
        results = []

        if search_directory:
            root = self.expand_path(search_directory)
            if not root or not os.path.exists(root):
                print(f"VEGETA FILE: Search directory not found -> {root}")
                return []
            self._search_root(root, name, results)
        else:
            roots = self._default_search_roots()
            for root in roots:
                self._search_root(root, name, results)
                if len(results) >= 100:
                    break

        print(f"VEGETA FILE: Found {len(results)} result(s) for -> {name}")
        return results[:100]

    def rename(self, old_path, new_name):
        old_path = self.expand_path(old_path)
        if not old_path or not os.path.exists(old_path):
            print(f"VEGETA FILE: Source not found -> {old_path}")
            return False
        new_name = str(new_name).strip()
        if not new_name:
            return False
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        if os.path.exists(new_path):
            print(f"VEGETA FILE: Destination already exists -> {new_path}")
            return False
        try:
            os.rename(old_path, new_path)
            print(f"VEGETA FILE: Renamed -> {old_path} -> {new_path}")
            return True
        except Exception as error:
            print(f"VEGETA FILE: Rename failed -> {error}")
            return False

    def move(self, source, destination):
        source = self.expand_path(source)
        destination = self.expand_path(destination)
        if not source or not os.path.exists(source):
            print(f"VEGETA FILE: Source not found -> {source}")
            return False
        if not destination or not os.path.isdir(destination):
            print(f"VEGETA FILE: Destination folder not found -> {destination}")
            return False
        try:
            shutil.move(source, destination)
            print(f"VEGETA FILE: Moved -> {source} -> {destination}")
            return True
        except Exception as error:
            print(f"VEGETA FILE: Move failed -> {error}")
            return False

    def delete(self, path):
        path = self.expand_path(path)
        if not path or not os.path.exists(path):
            print(f"VEGETA FILE: Path not found -> {path}")
            return False
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"VEGETA FILE: Deleted -> {path}")
            return True
        except Exception as error:
            print(f"VEGETA FILE: Delete failed -> {error}")
            return False

    def list_directory(self, path):
        path = self.expand_path(path)
        if not path or not os.path.isdir(path):
            print(f"VEGETA FILE: Directory not found -> {path}")
            return []
        results = []
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                results.append({
                    "name": item,
                    "path": full_path,
                    "type": "folder" if os.path.isdir(full_path) else "file",
                })
        except Exception as error:
            print(f"VEGETA FILE: List failed -> {error}")
        return results


file_manager = FileManager()
