FROM ubuntu:16.04

# docker build -t vanessa/flask-traits .

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python-pandas python-numpy

RUN pip install flask cognitiveatlas textblob

RUN mkdir -p /code
WORKDIR /code
ADD . /code

RUN python -c "import nltk; nltk.download('wordnet')"

ENTRYPOINT ["python"]
CMD ["/code/index.py"]
