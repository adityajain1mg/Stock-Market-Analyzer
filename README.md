Setup :

Go to project directory and run these commands

```
pipenv install
pipenv shell
```

To run in dev mode :

```
sanic app --host=127.0.0.1 --port=8000 --debug --reload
```


Available Routes :

```
v1/analyse/home
v1/analyse/historical-analysis
v1/analyse/compare
v1/analyse/real-time
```
