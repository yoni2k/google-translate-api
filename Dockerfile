FROM alpine

LABEL maintainer="yoni.test1234@gmail.com"

RUN apk add --no-cache python3 && python3 -m ensurepip

COPY . /google-translate-api

WORKDIR /google-translate-api

RUN pip3 install -r "requirements.txt"

EXPOSE 8080

# ENTRYPOINT "python3" "./src/translate.py"
ENTRYPOINT "sh"
