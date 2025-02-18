# Tutorial de Instalação

## Requisitos

- Python 3.12 ou superior (Usamos a versão 3.12.6 neste tutorial)
- Um navegador moderno (Chrome, Firefox, Edge, Opera, ...) (Usamos Fire-
    fox neste tutorial)
    O navegador deve ter JavaScript moderno ativado.
- 4 GB de RAM ou mais
- 1 GB de espaço livre em disco ou mais
- Processador de 2,5 GHz ou mais rápido (recomendado)
- Resolução de tela de 1440 x 900 ou superior (recomendado)
- Anaconda ou Miniconda instalados (Usamos Miniconda neste tutorial)

## Instalação

1.Instale o Python
    Você pode baixar o Python aqui.

2.Instale o Miniconda (ou Anaconda)
    Você pode instalar o Miniconda aqui.

3.Instale o Firefox (ou outro navegador moderno)
    Você pode baixar o Firefox aqui.

4.Instale o Git
    Você pode baixar o Git aqui.

5.Clone o repositório
```bash
$ git clone repository_url_here.git
```

6.Crie um novo ambiente
```bash
$ conda env create-f env.yml
```
```bash
$ conda activate mobenv
```

7.Faça as migrations
```bash
$ python manage.py makemigrations
```
```bash
$ python manage.py migrate
```

## Executando o servidor

```
$ python manage.py runserver
```

## Acessando a aplicação

Você pode acessar a aplicação através do link [http://localhost:8000/mobsinet/graph/](http://localhost:8000/mobsinet/graph/).




