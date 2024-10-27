# tiddler-export
## Description
exports each tiddler of a local [tiddlywiki](https://tiddlywiki.com/) file to a textfile with python and [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/)

This application is meant as a base for yor own tiddler export needs. Especially if you have many custom tiddler fields, tiddler images, etc this needs tweaking but can be a good base for starting.

As of now it reads all tiddlers which are content tiddlers (no $:/ in tiddlers title), reads title, text and tags and writes it as a string into the new file. Final files are .md or .txt. it also preserves the tiddlers creation and modified date in the newly exportet files

the resulting file name is cleaned of special characters (again, tweak to your own needs) and each tiddler is written into a seperate file in the export folder. If you need special transformation (like replacing tiddlywikis headings "!" with "#" you can tweak this)

* Tiddlywiki Homepage
  * https://tiddlywiki.com/
* List of basic tiddler fields for exporting
  * https://tiddlywiki.com/static/TiddlerFields.html


## Installation

* clone this repo
* cd into cloned repo folder
* create virtual environment

```powershell
python -m venv .venv
```

* activate environment
```powershell
python .\.venv\Scripts\Activate.ps1
```

* install requirements
```powershell
pip install -r requirements.txt
```

* deactivate environment
```powershell
deactivate.ps1
```

## Configuration
* apply your settings in the main.py

```python
tiddly_wiki_file = 'tiddlywiki.html' # name pf tiddlywiki to export files
ignore_types = ["image/png"] # ignore certain tiddler types
maximum_file_name_length = 220 # max length of file name
export_directory = "export" # name of folder where files will be stored. folder gets created if not exist
exportet_file_extension = "txt" # txt or md
exportet_file_tiddler_contents = ["title", "text", "tags"] # tiddler fields content, which get written in the exportet file
```

## Run Application
* copy your tiddlywiki.html file into the same folder as the main.py application
* run the application from the command line (or Visual Studio, etc)
```powershell
.venv/Scripts/python.exe ./main.py
```
* check created files in the export folder
