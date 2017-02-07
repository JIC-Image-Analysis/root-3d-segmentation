FROM jicscicomp/bioformats

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install jobarchitect
ADD scripts.tar.gz .
RUN rpm -ivh http://mirrors.ctan.org/support/texlive/texlive-dummy/EnterpriseLinux-7/texlive-dummy-2012a-1.el7.noarch.rpm &&  \
    yum install -y R
COPY install_r_packages.R .
RUN Rscript install_r_packages.R
