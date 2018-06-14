# datadog2wavefront
send dd-agent data to Wavefront.com via the [Wavefront Data Format](https://docs.wavefront.com/wavefront_data_format.html#wavefront-data-format-syntax) and [Wavefront Proxy](https://docs.wavefront.com/proxies.html)

## Install 
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

## dd-agent config
```yaml
dd_url: http://localhost:5060 # assumes the default port
```



