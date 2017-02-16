docker build -t ruter-telegram-bot
docker run -d -e TOKEN=[TELEGRAM TOKEN] --name rtb ruter-telegram-bot