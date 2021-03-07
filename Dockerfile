FROM python:3.8-slim-buster

ADD . /app
WORKDIR /app
RUN pip install pip==20.2.2
# RUN pip install -r requirements.txt
# RUN python setup.py install

CMD ["tail", "-f", "/dev/null"]
