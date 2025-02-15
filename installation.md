# Installation Tutorial

## Requirements

- Python 3.12 or higher (We use 3.12.6 in this tutorial)
- A modern browser (Chrome, Firefox, Edge, Opera, ...) (We use Firefox in this tutorial)
The browser need to have modern JavaScript enabled.
- 4 GB of RAM or more
- 1 GB of free disk space or more
- 2.5 GHz processor or faster (recommended)
- 1440 x 900 screen resolution or higher (recommended)
- Anaconda or Miniconda installed (We use Miniconda in this tutorial)

## Installation

1. Install Python
You can download Python from [here](https://www.python.org/downloads/).
2. Install Miniconda (or Anaconda)
You can install Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html).
3. Install Firefox (or another modern browser)
You can download Firefox from [here](https://www.mozilla.org/en-US/firefox/new/).
4. Install git
You can download git from [here](https://git-scm.com/download).
5. Clone the repository
```bash
$ git clone repository_url_here.git
```
6. Create a new environment
```bash
$ conda env create -f env.yml
```
```bash
$ conda activate mobenv
```

7. Making migrations
```bash
$ python manage.py makemigrations
```
```bash
$ python manage.py migrate
```

## Running the server

```bash
$ python manage.py runserver
```

## Accessing the application
You can access the application by going to [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/).