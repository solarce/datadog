# datadog
send dd-agent data to  influxdb and elasticsearch, so you can view dashboard and cofigure alert with grafana.

* metrics storage to influxdb
* ioStats storage to influxdb
* service checks storage to influxdb
* processes  storage to elasticsearch
* evnets  storage to elasticsearch
* resources  storage to elasticsearch
* system info  storage to elasticsearch
* dd-agent log storage to elasticsearch by logstash

## Install 
```bash
pip install -r requirements.txt
```

## RUN APP

```bash
gunicorn -c app.conf app:app
```

## dd-agent config
```yaml
dd_url: http://45.32.61.92:8080
```

## grafana

* url: http://openslack.com/
* username: test
* password: test


