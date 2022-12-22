FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/rubinghv/qbit-disco-bot.git 

RUN cat qbit-disco-bot/requirements.txt 
RUN pip3 install -r qbit-disco-bot/requirements.txt 


WORKDIR /app
