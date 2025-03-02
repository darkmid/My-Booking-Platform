FROM python:3.10.10-alpine3.17

COPY requirements.txt /
RUN pip install -r /requirements.txt --timeout=600 --index-url https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip install gevent gunicorn --timeout=600 --index-url https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
ADD . /flask
WORKDIR /flask

EXPOSE 3000

CMD ["gunicorn", "--worker-class", "gevent", "--workers", "2", "--bind", "0.0.0.0:3000", "wsgi:app"]