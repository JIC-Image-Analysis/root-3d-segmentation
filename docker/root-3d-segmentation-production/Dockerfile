FROM jicscicomp/bioformats

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install jobarchitect
ADD scripts.tar.gz .
