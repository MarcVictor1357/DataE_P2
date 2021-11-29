FROM ubuntu:20.04

ADD ./requirements.txt /home
ADD ./main.py /home
ADD ./ModelStrokeMF_P2_LR2.sav /home
ADD ./ModelStrokeMF_P2_KNN2.sav /home

WORKDIR /home

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r requirements.txt

EXPOSE 8000

CMD uvicorn main:strokepred_server --host 0.0.0.0
