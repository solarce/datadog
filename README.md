# datadog

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
gunicorn -w 4 -b 127.0.0.1:4000 -c app app:app
```


