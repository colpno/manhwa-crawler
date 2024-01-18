## About the project

The Manhwa Crawler project automates the crawling and retrieval of manhwa (Korean comics) from [acomics](acomics.net). It simplifies the process of downloading and organizing manhwa series for offline reading or other purposes.

Crawled data:
- Metadata Extraction: title, about, categories.
- Image Processing: cover, episode (chapter) contents.
- Organizational Structure: all text data are stored in `manhwa.json` and images are stored in each manhwa folder in `project/images`.




## Getting Started

### Prerequisites

- python3
- pip3
- virtualenv

### Installation

1. Clone the repo.
```sh
git clone git@github.com:colpno/crawlers.git
```

2. Create a python environment by using `virtualenv` and switching to it. Install `Python Environment Manager` extension if use VS Code and switch to the virtual environment
```sh
cd crawlers/acomicsdotnet
virtualenv env
```

3. Install required packages.
```python
pip install -r requirements.txt
```

### Usage

1. Run the script generator
```python
python3 script-generator/main.py
```

The url that has a table of manhwa can be given to the command
```python
python3 script-generator/main.py <url>
```

2. Run the script **(it's gonna take 30 seconds x number of manhwas)**
```sh
cd project && bash run.sh
```

### Note

> The metadata and images are stored in `project/data`