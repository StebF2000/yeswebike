# The build-stage image:
FROM continuumio/miniconda3

# Install the package as normal:
COPY docker/environment.yml .
RUN conda env create --file environment.yml nomkl && conda clean -afy && find /opt/conda/ -follow -type f -name '*.a' -delete && find /opt/conda/ -follow -type f -name '*.pyc' -delete && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# Copy data
COPY app/ /app/
COPY wsgi.py /
COPY get_data_on_time.py /

# Wait DB
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.2/wait /wait
RUN chmod +x /wait
