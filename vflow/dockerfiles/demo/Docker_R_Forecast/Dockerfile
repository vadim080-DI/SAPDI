FROM debian:9.4

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		locales \
	&& rm -rf /var/lib/apt/lists/*

## Install R
## Set a default CRAN repo
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		r-base \
		r-base-dev \
		r-recommended \
		libnlopt-dev \
		curl \
        && echo 'options(repos = c(CRAN = "https://cran.rstudio.com/"), download.file.method = "libcurl")' >> /etc/R/Rprofile.site \
	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds \
	&& rm -rf /var/lib/apt/lists/*

## Install additional R packages
RUN apt-get update
RUN apt-get install libcurl4-openssl-dev

RUN echo 'options(repos="https://cran.rstudio.com/", download.file.method = "libcurl")' >> /etc/R/Rprofile.site \
    && Rscript  -e "install.packages(c('Rserve'), dependencies=TRUE)" \
    && Rscript  -e "install.packages(c('jsonlite'), dependencies=TRUE)" \
    && Rscript  -e "install.packages(c('MLmetrics'), dependencies=TRUE)" \
    && Rscript  -e "install.packages(c('forecast'), dependencies=TRUE)" \
    && Rscript  -e "install.packages(c('lubridate'), dependencies=TRUE)" 