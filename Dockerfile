FROM ubuntu:18.04

ARG ACCESS_KEY
ARG SECRET_KEY

WORKDIR /usr/src/app

# RUN apk add --no-cache \
# 	python3 \
# 	py3-pip \
# 	curl \
# 	&& pip3 install --upgrade pip \
# 	&& pip3 install \
# 	awscli \
# 	&& rm -rf /var/cache/apk/*

RUN apt-get update && \
	apt-get install --no-install-recommends -y \
	python3.8 python3-pip python3.8-dev \
	lilypond \
	&& pip3 install --upgrade pip \
	&& pip3 install awscli

RUN printf "$ACCESS_KEY\n$SECRET_KEY\nus-west-1\n\n" | aws configure

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

RUN rm settings.json

RUN mv prod_settings.json settings.json

EXPOSE 4000

CMD ["python3", "-m", "notescribe"]