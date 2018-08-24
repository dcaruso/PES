FROM debian:9

RUN apt-get update && \
    apt-get install -y gcc g++ git iverilog make python python-dev gnat clang llvm zlib1g-dev gtkwave build-essential python-numpy

RUN git clone https://github.com/tgingold/ghdl.git ghdl_src/ \
 && cd ghdl_src \
 && ./configure --prefix=/usr/local --with-llvm-config \
 && make \
 && make install \
 && make clean \
 && cd .. \
 && rm -r ./ghdl_src --force

RUN git clone https://github.com/potentialventures/cocotb.git && chmod -R a+rw /cocotb

ENV COCOTB /cocotb

RUN apt-get install -y python-pip python-opencv python-tk

RUN pip install jupyter \
                matplotlib \
                scipy \
                ipython \
                Pillow \
                imutils

RUN apt-get install -y wget

RUN wget http://www.dilloneng.com/uploads/2/1/2/2/21220816/demodel-0.2.tar.gz

RUN tar -xvzf demodel-0.2.tar.gz

RUN cd deModel-0.2 && python setup.py install && cd ../ && rm -rf demodel-0.2

RUN useradd -ms /bin/bash pesuser

WORKDIR /home/pesuser
RUN git clone https://github.com/dcaruso/PES.git /home/pesuser/pes
RUN cd /home/pesuser/pes && git pull
RUN chown -R pesuser:pesuser /home/pesuser/pes
