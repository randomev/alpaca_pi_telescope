# Ascom Alpaca driver for Raspberry PI telescope mount 
Ascom Alpaca telescope driver for
Raspberry PI telescope interface for DIY tracking mount

Uses also motor-shield for Arduino Uno and repository from

https://github.com/randomev/TelescopeUno.git

Commands to create environment and install necessary items:

```
python3 -m venv venv
source venv/bin/activate
pip install -f requirements.txt
```

And then startup

```
python devices/app.py
```
