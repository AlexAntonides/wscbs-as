# set base image of the build stage
FROM python:3.8-slim-buster AS build_stage

# add the dependencies file to a temporary directory
ADD requirements.txt /tmp/

# update and install essential packages
RUN apt-get update \
    && apt-get install -y \
    build-essential

# install the dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r /tmp/requirements.txt

# set base image of the production stage
FROM python:3.8-slim-buster AS production_stage

# copy the build stage result to the production stage
COPY --from=build_stage /root/.local /root/.local

# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# create the app directory
RUN mkdir -p /app/
RUN pip install pytest

# set the work directory to the newly created directory.
WORKDIR /app/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]