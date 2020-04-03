# Imgur Downloader

<small>_Optimized for python 3.6_</small>

Project for downloading - in an semi-automatic way - solo images and complete 
albums from imgur. 

----------------------

## Dependencies

For installing the requirements, in your ___venv___ or ___anaconda env___, 
just run the following command:

```shell script
pip install -r requirements.txt
```

----------------

## Project's Structure

```bash 
.
└── imgur-album_downloader
    ├── data
    │   └── downloaded-images
    │       ├── img-1.jpg
    │       ├── ...
    │       └── img-25.jpg
    ├── docs
    │   └── CREDITS
    ├── src
    │   ├── __init__.py
    │   ├── helpers.py
    │   ├── imgur.py
    │   └── settings.json
    ├── tests
    │   └── unittests
    │       ├── __init__.py
    │       └── test_helpers.py
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```

### Directory description

- __data:__ The data dir. Group of non-script support files.
- __docs:__ The documentation dir.
- __src:__ The scripts & source code dir.
- __tests:__ The unittests dir.

-----------------------

## Usage Notes

Section aimed on clarifying some running issues.

### Running

For running it, at the `~/src` directory just run:

```shell script
python imgur.py 'imgur_url' 'filepath'
``` 

or, if importing it as a module, just run:
````python
from imgur import ImgurDownload

if __name__ == '__main__':
    ImgurDownload('imgur_url', 'filepath').__call__()
````

### JSON structure

````json
{
  "client_id": "client_id",
  "client_secret": "client_secret"
}
````

_obs: in order to run this application you must have a json file at `~/src/settings.json`. This json must follow the structure above._

---------------
