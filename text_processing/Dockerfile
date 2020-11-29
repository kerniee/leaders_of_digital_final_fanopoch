FROM tensorflow/tensorflow
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install wget unzip

WORKDIR /code
RUN wget http://vectors.nlpl.eu/repository/20/199.zip
RUN unzip -d 199 199.zip

RUN pip install smart_open asyncio websockets

COPY HackServer /code/
CMD python Server.py