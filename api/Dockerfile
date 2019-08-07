FROM python:alpine3.9 AS base
WORKDIR /app
ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT
ENV PATH="${PYROOT}/bin${PATH}"
ENV PIPENV_VENV_IN_PROJECT true
ENV PIP_NO_CACHE_DIR false

FROM base AS build
RUN pip install pipenv
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev build-base
COPY ./Pipfile ./Pipfile.lock /app/
RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile

FROM base AS dev
RUN apk --no-cache add libpq
COPY --from=build $PYROOT/lib/ $PYROOT/lib/
#COPY --from=build $PYROOT/bin/gunicorn $PYROOT/bin/ipython /usr/local/bin/
COPY ./ /app/
ENTRYPOINT [ "./manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]

