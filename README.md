# datadog2wavefront
send dd-agent data to Wavefront.com via the [Wavefront Data Format](https://docs.wavefront.com/wavefront_data_format.html#wavefront-data-format-syntax) and [Wavefront Proxy](https://docs.wavefront.com/proxies.html)



# Setup on a server

## Install the app
(assumes you are running as `ubuntu`, with `sudo` privileges)
```bash
sudo adduser --system --no-create-home --group datadog2wavefront
sudo mkdir /var/run/datadog2wavefront \
  /var/log/datadog2wavefront

mkdir /opt/datadog2wavefront
git clone https://github.com/solarce/datadog2wavefront /opt/datadog2wavefront

virtualenv /opt/datadog2wavefront
source /opt/datadog2wavefront/bin/activate
pip install -r requirements.txt

sudo chmod -R 770 /opt/datadog2wavefront \
  /opt/datadog2wavefront \
  /var/run/datadog2wavefront \
  /var/log/datadog2wavefront
sudo chown -R datadog2wavefront:ubuntu \
  /opt/datadog2wavefront \
  /var/run/datadog2wavefront \
  /var/log/datadog2wavefront

```

## Setup as an upstart service
```bash
sudo cp /opt/datadog2wavefront/upstart.conf.example /etc/init/datadog2wavefront.conf
sudo service datadog2wavefront status
```

## Run the app as a service
```bash
sudo service datadog2wavefront start
```

## Configure the app

## Run the App

# Run locally, for dev, testing, etc

## Install the app
```bash
pip install -r requirements.txt
```

## Configure App
```bash
cp app.conf.example app.conf # and tweak settings as needed
cp settings.py.example settings.py # and tweak settings as needed
```

## Run the App

```bash
gunicorn -c app.conf app:app
```

# dd-agent config
```yaml
dd_url: http://localhost:5060 # assumes the default port
```



