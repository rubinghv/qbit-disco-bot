FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/rubinghv/qbit-disco-bot.git 

WORKDIR /qbit-disco-bot

RUN cat requirements.txt 
RUN pip3 install -r requirements.txt 

COPY config.py config.py

CMD [ "python3", "-m", "discobot"]