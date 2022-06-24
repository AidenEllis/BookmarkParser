"""Bookmark Parser API by Aiden Ellis (https://github.com/AidenEllis)"""

from __future__ import annotations

from BookmarkParser.utils import timestamptoDateConverter
from typing import Iterable, Optional
from etils import epy
import collections
import dataclasses
import functools
import datetime
import textwrap
import pathlib
import types
import ujson
import sys


class Bookmarks:
    """
    Main Bookmarks Class in charge of handling setup, root management, path checker.
    """

    def __init__(self, filepath: str = None, browser: str = None):
        self.filepath = filepath
        self.browser = browser

    def setup(self):
        """
        Does all setup for the Class.
        :return: `bookmarksRoots`
        """

        BROWSERS = ['chrome', 'brave']

        if not self.filepath and not self.browser:
            raise Exception("You have to pass atleast one argument ('filepath', 'browser')")

        if self.browser.lower() not in BROWSERS:
            error_msg = f"Unfortunately, this module doesnt support the browser named '{self.browser}'. Please check " \
                        f"the name again or pass the 'filepath' argument \n\t\t   or request for support at " \
                        f"https://github.com/AidenEllis/BookmarkParser"

            if not self.filepath:
                raise Exception(error_msg)

        path = self.getBookmarksPath()
        return self.bookmarksRoots(path)

    @functools.lru_cache(None)
    def bookmarksRoots(self, path: pathlib.Path) -> BookmarkRoots:
        """
        Converts the json data to BookmarkObject, step 1
        :param path:
        :return:
        """
        with open(path, encoding='UTF-8') as file:
            data = ujson.loads(file.read())
            data = data["roots"]
            data['browser'] = self.browser

            DATA_BOOKMARK_BAR = data["bookmark_bar"]
            DATA_SYNCED = data["synced"]
            DATA_OTHER = data["other"]

            DATA_BOOKMARK_BAR['browser'] = self.browser
            DATA_SYNCED['browser'] = self.browser
            DATA_OTHER['browser'] = self.browser

            return BookmarkRoots(
                synced=BookmarkObject.parseJsonData(None, DATA_SYNCED),
                bookmark_bar=BookmarkObject.parseJsonData(None, DATA_BOOKMARK_BAR),
                other=BookmarkObject.parseJsonData(None, DATA_OTHER),
            )

    def getBookmarksPath(self) -> pathlib.Path:
        """Returns the default bookmark path depending on the OS."""

        BOOKMARKS_PATH = {
            "chrome": {
                "linux": "~/.config/google-chrome/Default/Bookmarks",
                "darwin": "~/Library/Application Support/Google/Chrome/Default/Bookmarks",
                "win32": "~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"
            },

            "brave": {
                "linux": "~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks",
                "darwin": "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks",
                "win32": "~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Bookmarks"
            }
        }

        path = None

        if not self.filepath and self.browser:
            path = BOOKMARKS_PATH.get(self.browser).get(sys.platform.lower())

        elif self.filepath:
            path = self.filepath

        path = pathlib.Path(path)
        path = path.expanduser()

        if not path.exists():
            raise ValueError(f"{path} not found.")
        return path


@dataclasses.dataclass(frozen=True)
class BookmarkRoots:
    """
    Bookmarks Root Selection Class
    """

    other: BookmarkFolder
    bookmark_bar: BookmarkFolder
    synced: BookmarkFolder


@dataclasses.dataclass(frozen=True)
class BookmarkObject:
    """
    Base for Bookmark Objects which also handles json parsing.
    """

    id: int
    name: str
    guid: str
    browser: str
    datetime: datetime.datetime
    parent: Optional[BookmarkFolder]

    @classmethod
    def parseJsonData(cls, parent, values):
        """
        Parses Input Json data and structures it.
        :return: _BookmarkObject
        """

        dataValue = types.SimpleNamespace(**values)
        browser = dataValue.browser

        _kwargs = dict(
            name=dataValue.name,
            datetime=timestamptoDateConverter(dataValue.date_added),
            parent=parent,
            guid=dataValue.guid,
            id=int(dataValue.id),
            browser=str(browser)
        )

        if dataValue.type == "url":
            return BookmarkUrl(url=dataValue.url, **_kwargs,)

        else:
            parent = BookmarkFolder(children=[], **_kwargs)
            dataList = []
            for values in dataValue.children:
                values['browser'] = browser
                dataList.append(BookmarkObject.parseJsonData(parent, values))

            parent.children.extend(dataList)
            return parent

    @functools.cached_property
    def path(self) -> str:
        """
        Returns the path of the Object (Folder, Urls)
        """

        bookmark = self
        parts = [self.name]

        while bookmark := bookmark.parent:
            parts.append(bookmark.name)

        return "/".join(reversed(parts))

    def is_folder(self) -> bool:
        """Checks if it's a folder or not (bool)"""
        return isinstance(self, BookmarkFolder)


@dataclasses.dataclass(frozen=True)
class BookmarkFolder(BookmarkObject):
    children: list[BookmarkUrl]

    @property
    def url(self) -> str:
        """
        Gives back the browser url of the bookmark item.
        """
        return f"{self.browser}://bookmarks/?id={self.id}"

    @functools.cached_property
    def folders(self) -> list[BookmarkFolder]:
        """
        Returns all the child folders (This does not contain any nested folders)

        📂 Self (Parent)
        ├── 📁 Child 1 ✔
        │   └── 📁 Child 1's child (1) ❌
        ├── 📁 Child 2 ✔
        │   ├── 📁 Child 2's child (1) ❌
        │   └── 📁 Child 2's child (2) ❌
        └──
        """

        return [v for v in self.children if isinstance(v, BookmarkFolder)]

    @functools.cached_property
    def urls(self) -> list[BookmarkUrl]:
        """
        returns all the urls within the current folder

        📂 Self (Parent)
        ├── 📁 Child 1
        │   └── 🔗 Link 1 ❌
        │   └── 🔗 Link 2 ❌
        │
        └── 🔗 Link 3 ✔
        └── 🔗 Link 4 ✔
        └── 🔗 Link 5 ✔
        └── 🔗 Link 6 ✔
        """

        return [v for v in self.children if isinstance(v, BookmarkUrl)]

    @functools.cached_property
    def nestedUrls(self) -> list[BookmarkUrl]:
        """
        returns all the urls within the current folder and also from the nested folders.

        📂 Self (Parent)
        ├── 📁 Child 1
        │   └── 🔗 Link 1 ✔
        │   └── 🔗 Link 2 ✔
        │
        └── 🔗 Link 3 ✔
        └── 🔗 Link 4 ✔
        └── 🔗 Link 5 ✔
        └── 🔗 Link 6 ✔
        """

        result = []

        result.extend(self.urls)

        for f in self.folders:
            result.extend(f.nestedUrls)

        return result

    @functools.cached_property
    def num_urls(self) -> int:
        """
        Returns the total amount of urls within the current folder. (this does not contains urls from nested folders)
        """
        return sum(f.num_urls for f in self.folders) + len(self.urls)

    @functools.cached_property
    def num_subfolders(self) -> int:
        """
        Returns the total number of subfolders (including child and nested folders)
        """

        if not self.folders:
            return 0
        else:
            return sum(f.num_subfolders + 1 for f in self.folders)

    @functools.cached_property
    def num_folders(self) -> int:
        """
        Returns the total number of only child folders.
        """
        return len([v for v in self.children if isinstance(v, BookmarkFolder)])

    @functools.cached_property
    def subfolders(self) -> list:
        """
        Returns all of the child and its nested subfolders within the chosen directory.

        📂 Self (Parent)
        ├── 📁 Child 1 ✔
        │   └── 📁 Child 1's child (1) ✔
        ├── 📁 Child 2 ✔
        │   ├── 📁 Child 2's child (1) ✔
        │   └── 📁 Child 2's child (2) ✔
        │       └── 📁 Child 2's child (2)'s child(1) ✔
        └──
        """

        result = []

        result.extend(self.folders)

        for f in self.folders:
            result.extend(f.subfolders)

        return result

    @functools.cached_property
    def _nameToChildren(self) -> dict[str, list[BookmarkObject]]:
        """Returns the mapping name --> children (name can be duplicate)."""
        nameToChildren = collections.defaultdict(list)

        for b in self.children:
            nameToChildren[b.name].append(b)

        return nameToChildren

    def __iter__(self) -> Iterable[BookmarkObject]:
        """Iterate over all children."""
        return iter(self.children)

    def __getitem__(self, value: str) -> BookmarkObject:
        children = self._nameToChildren[value]
        if len(children) > 1:
            raise KeyError(f"Duplicated key found: {value} (bookmarks have the same name)")
        (item,) = children
        return item

    def __repr__(self) -> str:
        children = epy.Lines()
        children += "children=["

        with children.indent():
            for child in self.children:
                if isinstance(child, BookmarkFolder):
                    line = f"📂 -> '{child.name}'/ ({child.num_urls} urls) ({child.num_subfolders} Total " \
                           f"Folder{'s'[:child.num_subfolders ^ 1]} inside --> {child.num_folders} " \
                           f"folder{'s'[:child.num_subfolders ^ 1]} + {child.num_subfolders - child.num_folders} " \
                           f"nested subfolder{'s'[:int(child.num_subfolders - child.num_folders) ^ 1]})"
                else:
                    url = textwrap.shorten(child.url, width=100, placeholder=f"{child.url[0:35]}...")
                    line = f"🔗 -> ({url})"
                children += line

        children += "],"

        lines = epy.Lines()
        lines += f"{type(self).__name__}("

        with lines.indent():
            lines += f"⚫ name={self.name!r},"
            lines += f"⚫ path={self.path!r},"
            lines += f"⚫ url={self.url!r},"
            lines += f"⚫ datetime={self.datetime},"
            lines += f"⚫ num_urls={self.num_urls},"
            lines += f"⚫ num_folders={self.num_folders}"
            lines += f"⚫ num_subfolders={self.num_subfolders}"
            lines += children.join()

        lines += ")"

        return lines.join()


@dataclasses.dataclass(frozen=True)
class BookmarkUrl(BookmarkObject):
    url: str

    def __repr__(self) -> str:
        lines = epy.Lines()
        lines += f"{type(self).__name__}("

        with lines.indent():
            lines += f"name={self.name!r},"
            lines += f"url={self.url!r},"
            lines += f"dir_path={str(self.path).replace(self.name, '')[0:-1]!r},"
            lines += f"datetme={self.datetime},"

        lines += ")"

        return lines.join()
