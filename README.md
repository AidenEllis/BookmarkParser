<a href="https://github.com/AidenEllis/Cligo"><p align="center"></a>
<img src="https://voxelmax.com/assets/testimonial-william-santacruz.jpg" height="auto" width="200" style="border-radius:10%"/>

<p align="center">
  <strong>Bookmark Parser - Explore Your Browser Bookmark Data 🚀</strong>
</p>

<h3 align="center">
  <a href="https://github.com/AidenEllis/BookmarkParser/blob/main/CODE_OF_CONDUCT.md">COC</a>
  <span> · </span>
  <a href="https://discord.gg/EZ3SspPZ93">Community</a>
  <span> · </span>
  <a href="#">Docs (Below)</a>
</h3>

## 🎫 Introduction :
The main goal of BookmarkParser Module is to allow people to easily explore and play with their bookmarks' data in an 
easy-structured way with a variety of functionality.


## ⚫ Browsers tested on: 
* `Google Chrome`
* `Brave`

### Installing BookmarkParser :

`via pip (recommended) :`
```shell
pip install BookmarkParser
```

or

`via pip + github : `
```shell
pip install git+https://github.com/AidenEllis/BookmarkParser.git
```

## 🤓 Docs:

Let's import the moduele and show you along :

```python
from BookmarkParser import Bookmarks

bookmarks = Bookmarks()
```

#### 🥨 Bookmarks class:
* Arguments: 
  * `filepath: str`: file path of the Bookmarks file. Usually used for manually assign a file. Google it with your specific browser brand.
  ####
  * `browser: str`: Automatically finding your browser file path. Currently, only works with `'Chrome', 'Brave'` just pass in either of these browser name and it'll find the `Bookmarks` file.


Setting up out Class

```python
from BookmarkParser import Bookmarks

bookmarks = Bookmarks(browser='Chrome').setup()  # Automatic Path setup
# or
bookmarks = Bookmarks(filepath="C://File/to/somewhere/Bookmarks").setup()  # Manual File setup

```

Let's actually use it

```python
from BookmarkParser import Bookmarks

bookmarks = Bookmarks(filepath="C://File/to/somewhere/Bookmarks").setup()  # Manual File insert

a = bookmarks.bookmark_bar  # --> List
b = bookmarks.synced        # --> List
c = bookmarks.other        # --> List

# These are the 3 types of ROOT Bookamarks Folder
```

you can iterate through it

```python
from BookmarkParser import Bookmarks

bookmarks = Bookmarks(filepath="C://File/to/somewhere/Bookmarks").setup()  # Manual File insert

for bookmark in bookmarks.bookmark_bar:
  print(bookmark) # Returns a list of Bookmarked items (urls and folders)
```

> `BookmarkFolder` Attribute & Attributes Functions :
* `name`: Name of the folder or the link
###
* `path`: Path to the bookmarked item e.g. "Bookmarks/bookmarks_tab/title"
###
* `url` : Returns url of the bookmarked item (different urls for folders and links)
###
* `datetime`: Returns the date-time of when it was added
###
* `children` (only available for folders) (returns urls and child folders)
###
* `is_folder`: Cheks the if the bookmark item is folder or not.
###
* `url`: Gives back the browser url of the bookmark item.
###
* `urls`: returns all the urls (objects) within the current folder

        📂 Self (Parent)
        ├── 📁 Child 1
        │   └── 🔗 Link 1 ❌
        │   └── 🔗 Link 2 ❌
        │
        └── 🔗 Link 3 ✔
        └── 🔗 Link 4 ✔
        └── 🔗 Link 5 ✔
        └── 🔗 Link 6 ✔
###
* `num_urls`: Returns the total amount of urls within the current folder. (this does not contains urls from nested folders)
###
* `nestedUrls`: returns all the urls within the current folder and also from the nested folders.

        📂 Self (Parent)
        ├── 📁 Child 1
        │   └── 🔗 Link 1 ✔
        │   └── 🔗 Link 2 ✔
        │
        └── 🔗 Link 3 ✔
        └── 🔗 Link 4 ✔
        └── 🔗 Link 5 ✔
        └── 🔗 Link 6 ✔
###
* `folders`: Returns all the child folders (This does not contain any nested folders)

        📂 Self (Parent)
        ├── 📁 Child 1 ✔
        │   └── 📁 Child 1's child (1) ❌
        ├── 📁 Child 2 ✔
        │   ├── 📁 Child 2's child (1) ❌
        │   └── 📁 Child 2's child (2) ❌
        └──
###
* `num_folders`: Returns the total number of only child folders.
###
* `subfolders`: Returns all the child and its nested subfolders within the chosen directory.

        📂 Self (Parent)
        ├── 📁 Child 1 ✔
        │   └── 📁 Child 1's child (1) ✔
        ├── 📁 Child 2 ✔
        │   ├── 📁 Child 2's child (1) ✔
        │   └── 📁 Child 2's child (2) ✔
        │       └── 📁 Child 2's child (2)'s child(1) ✔
        └──
###
* `num_subfolders`: Returns the total number of subfolders (including child and nested folders)

#### Here, have a cookie (づ｡ ◕‿‿◕｡) づ🍪
