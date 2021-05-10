# The build-stage image:
FROM continuumio/miniconda3

# Install the package as normal:
COPY docker/environment.yml .
RUN conda env create --file environment.yml nomkl && conda clean -afy && find /opt/conda/ -follow -type f -name '*.a' -delete && find /opt/conda/ -follow -type f -name '*.pyc' -delete && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# Copy data
COPY app/ data/app/
COPY data/estacions_bicing.csv data/data/
COPY wsgi.py data/

# Activate environement
WORKDIR /data
ENTRYPOINT [ "conda", "run", "-n", "yeswebike", "python", "wsgi.py" ]
