FROM ubuntu
WORKDIR /home
RUN apt-get update
RUN apt-get install -y net-tools netcat tcpdump inetutils-ping python3
RUN useradd -ms /bin/bash macbookpro
USER macbookpro
CMD ["/bin/bash"]