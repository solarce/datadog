import time, zlib,json, socket, sys
import settings

"""
Wavefront Data Format Syntax
<metricName> <metricValue> [<timestamp>] source=<source> [pointTags]
Valid Metrics
 - request.count 1001 source=test.wavefront.com
 - system.cpu.loadavg.1m 0.03 1382754475 source=test1.wavefront.com
 - marketing.adsense.impressions 24056 source=campaign1
 - new-york.power.usage 42422 source=localhost datacenter="dc1"
"""

def build_tag_string(tags, skip_tag_key):
  """
  Builds a string of tag_key=tag_value ... for all tags in the tags
  dictionary provided.  If tags is None or empty, an empty string is
  returned.
  Arguments:
  tags - dictionary of tag key => tag value
  skip_tag_key - skip tag named this (None to not skip any)
  """

  if not tags:
    return ''

  tag_str = ''
  for tag_key, tag_value in tags.iteritems():
    if not isinstance(tag_value, basestring) or tag_key == skip_tag_key:
      continue
    tag_str = tag_str + ' "%s"="%s"' % (tag_key, tag_value)

  return tag_str

def wf_formatter(point):
  metric_prefix = settings.WAVERONT_METRIC_PREFIX

  if not metric_prefix:
    metric_name = point['metric_name']
  else:
    metric_name = metric_prefix + point['metric_name']
  metric_value = point['metric_value']
  timestamp = point['timestamp']
  source = point['source']
  point_tags = build_tag_string(point['point_tags'], None)

  line = ('%s %s %d source="%s"%s' %
          (metric_name, metric_value, long(timestamp), source, point_tags))

  if settings.LOG_LEVEL == "debug":
    print(line)

  return line

def wf_outputter(line):
  proxy_host = settings.WAVEFRONT_PROXY_HOST
  proxy_port = settings.WAVEFRONT_PROXY_PORT

  if settings.LOG_LEVEL == "debug":
    print('Using Wavefront Proxy: %s:%s' % (proxy_host, proxy_port))
    print(line)

  # connect to the proxy
  sock = socket.socket()
  sock.settimeout(10.0)
  try:
    sock.connect((proxy_host, proxy_port))
  except socket.error as sock_err:
    err_str = (
        'Wavefront Emitter: Unable to connect %s:%d: %s' %
        (proxy_host, proxy_port, str(sock_err)))
    print err_str

  sock.sendall('%s\n' % (line))
  # close the socket (if open)
  if sock is not None:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def check_item_to_point(check_item):

  point = {
    "metric_name": "",
    "metric_value": 0,
    "timestamp": int(time.time()),
    "source": "",
    "point_tags": {}
  }

  point['metric_name'] = check_item['check']
  point['metric_value'] = check_item['status']
  point['timestamp'] = check_item['timestamp']
  point['source'] = check_item['host_name']
  if 'tags' in check_item:
    for tag in check_item['tags']:
      tag = tag.split(':')
      # some dd tags don't have a value and so we ignore them
      if len(tag) == 2:
        point['point_tags'][tag[0]] = tag[1]

  if settings.LOG_LEVEL == "debug":
    print(point)

  return point

def series_item_to_point(series_item,):

  point = {
    "metric_name": "",
    "metric_value": 0,
    "timestamp": int(time.time()),
    "source": "",
    "point_tags": {}
  }

  point['metric_name'] = series_item['metric']
  point['metric_value'] = series_item['points'][0][1]
  point['timestamp'] = series_item['points'][0][0]
  point['source'] = series_item['host']

  if 'tags' in series_item:
    if series_item['tags'] != None:
      for tag in series_item['tags']:
        tag = tag.split(':')
        # some dd tags don't have a value and so we ignore them
        if len(tag) == 2:
          point['point_tags'][tag[0]] = tag[1]

  if settings.LOG_LEVEL == "debug":
    print(point)
  return point

def process_request(request):

  # handle /api/v1/check_run/ metrics
  if 'check_run' in request.path:
    # metrics that are not encoded, usually means json
    if request.content_encoding is None:
      dd_data = request.get_json()
      check_item = dd_data[0]
      if check_item['check'].split('.')[0] == 'datadog':
        # skip metrics that start with 'datadog.
        pass
      else:
        wf_outputter(wf_formatter(check_item_to_point(check_item)))

    # metrics that are zlib compressed
    elif request.content_encoding == 'deflate':
      dd_data = json.loads(zlib.decompress(request.data))
      for check_item in dd_data:
        if check_item['check'].split('.')[0] == 'datadog':
          # skip metrics that start with 'datadog.
          pass
        else:
          wf_outputter(wf_formatter(check_item_to_point(check_item)))

  # handle /api/v1/series(/) metrics
  elif 'series' in request.path:

    if settings.LOG_LEVEL == "debug":
      print("series")

    # metrics that are not encoded, usually means json
    if request.content_encoding is None:

      if settings.LOG_LEVEL == "debug":
        print("json data")
      dd_data = request.get_json()

      # handle objects that begin with 'series'
      if 'series' in dd_data:
        series = dd_data['series']
        for series_item in dd_data['series']:
          if series_item['metric'].split('.')[0] == 'datadog':
            # skip metrics that start with 'datadog.
            pass
          else:
            wf_outputter(wf_formatter(series_item_to_point(series_item)))

    # metrics that are zlib compressed
    elif request.content_encoding == 'deflate':

      if settings.LOG_LEVEL == "debug":
        print("binary data")
      dd_data = json.loads(zlib.decompress(request.data))

      # handle objects that begin with 'series'
      if 'series' in dd_data:
        series = dd_data['series']
        for series_item in dd_data['series']:
          if series_item['metric'].split('.')[0] == 'datadog':
            # skip metrics that start with 'datadog.
            pass
          else:
            wf_outputter(wf_formatter(series_item_to_point(series_item)))

    # if there's another payload besides the one beginning with 'series'
    # then dump it out
    else:
      print("unknown payload data to series api")
      if request.content_encoding == 'deflate':
        dd_data = json.loads(zlib.decompress(request.data))
      else:
        dd_data = request.get_json()
      print(dd_data)

  # handle /intake/ metrics
  elif 'intake' in request.path:
    pass
    """
    the /intake endpoint is a legacy one and based on the data sent to it, as seen
    in https://github.com/DataDog/dd-agent/blob/master/tests/core/fixtures/payloads/legacy_payload.json
    I don't think we need to do anything with this data, if we do,
    we can uncomment this code below and fine tune 
    if request.content_encoding == 'deflate'
      print("intake")
      print("binary data")
      dd_data = json.loads(zlib.decompress(request.data))
      dd_data['processes'] == None
      for key, val in dd_data.items():
        if key == 'processes':
          print("skipping because its looong.")
        else:
          print("{} = {}".format(key, val))
    """

  # finally, dump anything we haven't seen
  else:
    if settings.LOG_LEVEL == "debug":
      print("dunno what the data is, check it out")
      print(request.content_encoding)
      print(request.path)
      if request.content_encoding == 'deflate':
        dd_data = json.loads(zlib.decompress(request.data))
      else:
        dd_data = request.get_json()
      print(dd_data)
    pass