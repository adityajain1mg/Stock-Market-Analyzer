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
v1/analyse/historical?stock={}&duration={}&candle-size={}
v1/analyse/compare?stock={}&stock={}&duration={}&candle-size={}
v1/analyse/realtime?stock={}
```
