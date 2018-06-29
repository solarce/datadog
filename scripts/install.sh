#!/usr/bin/env bash

cd /opt/datadog2wavefront

echo "Adding 'datadog2wavefront' user"
sudo adduser --system --no-create-home --group datadog2wavefront
echo "Creating pid and logging directory"
sudo mkdir /var/run/datadog2wavefront \
  /var/log/datadog2wavefront

echo "Setting up virtualenv and installing dependencies"
virtualenv /opt/datadog2wavefront
source /opt/datadog2wavefront/bin/activate
pip install -r requirements.txt

echo "Setting permissions for upstart service to be happy"
sudo chmod -R 770 /opt/datadog2wavefront \
  /var/run/datadog2wavefront \
  /var/log/datadog2wavefront
sudo chown -R datadog2wavefront:ubuntu \
  /opt/datadog2wavefront \
  /var/run/datadog2wavefront \
  /var/log/datadog2wavefront