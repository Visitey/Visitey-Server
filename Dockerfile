FROM ubuntu:17.10

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Adding Pipfiles
ONBUILD COPY Pipfile Pipfile
ONBUILD COPY Pipfile.lock Pipfile.lock

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

# Copy files
COPY media ./Visitey-Server/media
COPY rest_auth ./Visitey-Server/rest_auth
COPY rest_friendship ./Visitey-Server/rest_friendship
COPY rest_group ./Visitey-Server/rest_group
COPY rest_htags ./Visitey-Server/rest_htags
COPY rest_profile ./Visitey-Server/rest_profile
COPY rest_social ./Visitey-Server/rest_social
COPY static ./Visitey-Server/static
COPY staticfiles ./Visitey-Server/staticfiles
COPY visitey_backend ./Visitey-Server/visitey_backend
COPY Pipfile ./Visitey-Server/Pipfile
COPY Pipfile.lock ./Visitey-Server/Pipfile.lock
COPY Procfile ./Visitey-Server/Profile
COPY Procfile.windows ./Visitey-Server/Procfile.windows
COPY manage.py ./Visitey-Server/manage.py
COPY requirements.txt ./Visitey-Server/requirements.txt
COPY install_postgis.sh ./Visitey-Server/install_postgis.sh

# -- Install Pipenv:
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN cd ./Visitey-Server && ./install_postgis.sh && pip install -r requirements.txt && ./db_install.sh  && python3 manage.py test

# Define default command.
CMD ["bash"]
