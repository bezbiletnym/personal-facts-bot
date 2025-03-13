# Facts Bot

I love interesting facts, but I don't like to browse websites from my phone.
So I made this little project to send articles from https://nowiknow.com/ to my Telegram account through a chatbot API.

Main script is searching for a *config.yaml* file. So before launching the script you need to fill in *BOT_TOKEN* and *CHAT_ID* fields in *config_template.yaml* and rename it.

I launch it as a scheduled task on [PythonAnywhere](https://www.pythonanywhere.com/) via the following bash script:
```
#!/bin/bash

cd /home/bankir35/facts-bot/personal-facts-bot
. venv/bin/activate
python ./main.py
```