FROM rocker/rstudio:4.3

RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
        libxml2-dev \
        libssl-dev  \
        libcurl4-openssl-dev \
        libfontconfig1-dev \
        libcairo2-dev \
        libicu-dev \
        libz-dev \
        unzip \
        zip \
        liblzma-dev \
        libbz2-dev \
        libglpk-dev \
        libharfbuzz-dev \ 
        libfribidi-dev \
        libfreetype6-dev \ 
        libpng-dev \ 
        libtiff5-dev \ 
        libjpeg-dev \
        libgit2-dev


RUN R -e "install.packages(c('devtools'))"
RUN R -e "install.packages(c('plyr','data.table','pander','ggthemes','ggplot2','scales','argparse'))"
RUN R -e "install.packages(c('BiocManager'))"

RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
        cmake

RUN R -e "library(BiocManager); BiocManager::install(c('FSA'))"
RUN R -e "library('devtools'); install_github('trinker/plotflow')"
RUN R -e "install.packages(c('svglite'))"
RUN R -e "library('devtools'); install_github('dphiggs01/wormcat')"

RUN apt-get update -q && \
    apt-get install -y --no-install-recommends \
         python3-pip

RUN pip3 install wormcat_batch xlsxwriter pandas --no-input

# Create user and setup permissions on /etc/sudoers
RUN echo "rstudio ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers && \
    chmod 0440 /etc/sudoers && \
    chmod g+w /etc/passwd 


