FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN rm settings.json

RUN mv prod_settings.json settings.json

EXPOSE 4000

CMD ["python", "-m", "notescribe"]