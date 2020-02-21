FROM ubuntu:18.04
MAINTAINER choikoal "junyoung_choi@tmax.co.kr"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /flask_exercise
WORKDIR /flask_exercise
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_sample.py"]
