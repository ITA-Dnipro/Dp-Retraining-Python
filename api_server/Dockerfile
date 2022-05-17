FROM python:3.10-alpine3.15
# 
RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/
# 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/"
#
RUN apk update
RUN apk add --no-cache \
git \
postgresql-dev \
gcc \
python3-dev \
musl-dev \
libressl-dev \
libffi-dev \
zeromq-dev
#
COPY . /usr/src/app/
# 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#
CMD ["/usr/src/app/entrypoint.sh"]
