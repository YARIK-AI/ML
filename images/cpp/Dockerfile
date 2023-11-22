FROM debian:12.1

RUN  apt-get update -y && \
  apt-get install -yq --no-install-recommends locales locales-all 

ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
ENV TZ Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y build-essential gdb 

#создание пользователя
RUN adduser --disabled-password --gecos '' sdl
WORKDIR /home/sdl

#графическое окно Qt
RUN apt-get install -y qt6-base-dev

RUN apt-get install -y libopencv-dev

#USER sdl
