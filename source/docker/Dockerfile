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
ENV WAIT_FOR_VERSION=v0.0.3
RUN wget "https://github.com/ArcanjoQueiroz/wait-for/releases/download/${WAIT_FOR_VERSION}/wait-for" && chmod u+x wait-for

CMD [ "conda", "run", "-n", "yeswebike", "python", "wsgi.py", "&&", "conda", "run", "-n", "yeswebike", "python", "get_data_on_time.py" ]
