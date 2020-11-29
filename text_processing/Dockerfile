FROM tensorflow/tensorflow
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY HackServer /code/
RUN pip freeze
CMD python Server.py