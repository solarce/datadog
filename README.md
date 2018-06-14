# datadog2wavefront
send dd-agent data to Wavefront.com via the [Wavefront Data Format](https://docs.wavefront.com/wavefront_data_format.html#wavefront-data-format-syntax) and [Wavefront Proxy](https://docs.wavefront.com/proxies.html)



## Setup on a server

### Install the app
(assumes you are running as `ubuntu`, with `sudo` privileges)
```bash
sudo mkdir /opt/datadog2wavefront
sudo chown ubuntu /opt/datadog2wavefront
git clone https://github.com/solarce/datadog2wavefront /opt/datadog2wavefront

cd /opt/datadog2wavefront
./scripts/install.sh
```

### Setup as an upstart service
(assumes you are running as `ubuntu`, with `sudo` privileges)
```bash
cd /opt/datadog2wavefront

cp app.conf.example app.conf # tweak settings as needed

cp settings.py.example settings.py # tweak settings as needed

sudo chown datadog2wavefront:ubuntu app.conf settings.py

sudo cp /opt/datadog2wavefront/upstart.conf.example /etc/init/datadog2wavefront.conf

sudo service datadog2wavefront status
```

### Run the app as a service
```bash
sudo service datadog2wavefront start
```

## Run locally, for dev, testing, etc

### Install the app
```bash
pip install -r requirements.txt
```

### Configure App
```bash
cp app.conf.example app.conf # and tweak settings as needed
cp settings.py.example settings.py # and tweak settings as needed
```

### Run the App
(will output logging to shell)
```bash
gunicorn -c app.conf app:app
```

----

## dd-agent config
```yaml
dd_url: http://localhost:5060 # assumes the default port
```



