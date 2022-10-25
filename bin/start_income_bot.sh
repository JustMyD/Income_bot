#!/bin/bash
cd /home/www/Bot_projects/Income_bot
source /home/www/.virtualenvs/income_bot/bin/activate
pip list
python3 src/income_bot.py
