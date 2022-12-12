FROM mongo:latest
RUN apt update && apt install -y curl unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
WORKDIR /tmp/
RUN unzip awscliv2.zip
RUN ./aws/install
COPY ./script.sh /
WORKDIR /
RUN chmod +x script.sh
CMD ["/script.sh"]