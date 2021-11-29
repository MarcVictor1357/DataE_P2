FROM debian:latest

RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install datetime
# && pip3 install time

ADD test.py /my_tests/test.py

WORKDIR /my_tests/

# No port to expose from this container :
# EXPOSE 8000

CMD python3 test.py
