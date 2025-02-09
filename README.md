# MobENV

### Comandos para exportar dependências

```bash
$ conda env export --no-builds | grep -v "^prefix:"  > environment.yml
```
```bash
$ conda env export | grep -v "^prefix:" | sed -E 's/(=.+)//' > environment-noversion.yml
```
```bash
$ conda env export | grep -v "^prefix:" > environment-builds.yml 
```

## Admin password
user: root
pass: root