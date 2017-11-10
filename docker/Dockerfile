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

