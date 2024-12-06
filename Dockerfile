FROM python:3.10
WORKDIR /root/Mikobot

COPY . .

RUN apt-get install -y ffmpeg python3-pip curl
RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

EXPOSE 8000
CMD python -m Mikobot