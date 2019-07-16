# Just opens a shell with all prerequisites
# From shell need to:
# 1. Update resources/token.txt
# 2. Run either src/translate.py or tests/test_translate.py - see more info in README.md

FROM alpine

LABEL maintainer="yoni.test1234@gmail.com"

RUN apk add --no-cache python3 && python3 -m ensurepip

COPY . /google-translate-api

WORKDIR /google-translate-api

RUN pip3 install -r "requirements.txt"

# EXPOSE 8080 - not necessary, not exposing HTTP service currently

# CMD ["python3","-u","./translate.py"] - must be done from within 'src' directory

