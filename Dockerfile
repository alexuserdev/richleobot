FROM python:3.8

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"


WORKDIR /app
COPY bot.py requirements* /app/
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt
ADD . /app/

RUN ["chmod", "+x", "/app/scripts/bot-entrypoint.sh"]
ENTRYPOINT bot-entrypoint.sh


