# MobENV

## Getting Started

1. Requirements:
You need to have a modern browser (Chrome, Firefox, Edge, Opera, ...)

2. Install conda
You can install anaconda or miniconda. We will use miniconda.

3. Create a new environment
    ```bash
    $ conda env create -f env.yml
    ```
    ```bash
    $ conda activate mobenv
    ```

4. Making migrations
    ```bash
    $ python manage.py makemigrations
    ```
    ```bash
    $ python manage.py migrate
    ```

5. Run server
    ```bash
    $ python manage.py runserver
    ```

6. Open browser and go to [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/)
---
### Commands to export dependencies

```bash
$ conda env export --no-builds | grep -v "^prefix:"  > environment.yml
```
```bash
$ conda env export | grep -v "^prefix:" | sed -E 's/(=.+)//' > environment-noversion.yml
```
```bash
$ conda env export | grep -v "^prefix:" > environment-builds.yml 
```

###  Admin password
user: root
pass: root