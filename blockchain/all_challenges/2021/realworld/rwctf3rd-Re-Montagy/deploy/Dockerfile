FROM ubuntu:18.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y python3 python3-pip xinetd vim

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome web3 py-solc-x
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple sty
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple tqdm
RUN pip3 install colorfulpanda

#RUN python3 -m solcx.install v0.5.10

RUN apt-get install -y netcat net-tools
RUN mkdir /root/ethbot
RUN mkdir /root/log

COPY ./ethbot /root/ethbot
COPY ./start.sh /root/start.sh
COPY ./ctf.xinetd /etc/xinetd.d/ctf
#COPY ./solc-v0.5.11 /root/.solcx/solc-v0.5.11


EXPOSE 10101

ENTRYPOINT ["/root/start.sh"]
#ENTRYPOINT ["/bin/bash"]
