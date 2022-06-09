FROM node:18.1.0-alpine
# 
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
#
COPY . /usr/src/app/
#
RUN npm install
RUN npm install react-scripts@5.0.1 -g
