FROM ubuntu:18.04
MAINTAINER jjeon "joonha_jeon@tmax.co.kr"
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3.7 python3.7-dev python3-pip python3-setuptools python3-wheel gcc
COPY . /dfa_module
WORKDIR /dfa_module
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["flask_sample.py"]
