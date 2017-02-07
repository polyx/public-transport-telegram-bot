# Telegram bot for public transport in oslo

This bot will accept your location and than give you a list of nearby stops. Upon choosing one stop you will be given 
10 soonest departures from the choosen stop.

This bot is based on the telepot library for interacting with the telegram bot api.

## How to run

`docker run -it --rm -e TOKEN=[TELEGRAM TOKEN] ruter-telegram-bot`

or run as daemon
 
 `docker run -d -e TOKEN=[TELEGRAM TOKEN] --name <someName> ruter-telegram-bot`