FROM python:3.11

WORKDIR /opt/app/

ENV PYTHONPATH=/opt/app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python
