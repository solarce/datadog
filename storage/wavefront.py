import time, zlib,json

# Wavefront Data Format Syntax
# <metricName> <metricValue> [<timestamp>] source=<source> [pointTags]
# Valid Metrics
# - request.count 1001 source=test.wavefront.com
# - system.cpu.loadavg.1m 0.03 1382754475 source=test1.wavefront.com
# - marketing.adsense.impressions 24056 source=campaign1
# - new-york.power.usage 42422 source=localhost datacenter="dc1"

def wf_formatter(metric_name, metric_value, timestamp, source, point_tags):
  line = ('%s %s %d source="%s"%s' %
          (metric_name, metric_value, long(timestamp), source, point_tags))
  #line = ('%s %s %d source="%s"%s' %
  #        (name, value, long(tstamp), host_name, tag_str))
  return line

def check_to_point(check_data, v = False):

  point = {
    "metric_name": "",
    "metric_value": 0,
    "timestamp": int(time.time()),
    "source": "",
    "point_tags": {}
  }

  point['metric_name'] = check_data['check']
  point['metric_value'] = check_data['status']
  point['timestamp'] = check_data['timestamp']
  point['source'] = check_data['host_name']
  if 'tags' in check_data:
    for tag in check_data['tags']:
      tag = tag.split(':')
      # some dd tags don't have a value and so we ignore them
      if len(tag) == 2:
        point['point_tags'][tag[0]] = tag[1]
  if v == True:
    print(point)
  return point

def series_item_to_point(series_item, v = False):

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

  if v == True:
    print(point)
  return point

def process_request(request):

  # handle /api/v1/check_run/ metrics
  if 'check_run' in request.path:
    # metrics that are not encoded, usually means json
    if request.content_encoding == None:
      dd_data = request.get_json()
      dd_data = dd_data[0]
      check_to_point(dd_data)

    # metrics that are zlib compressed
    elif request.content_encoding == 'deflate':
      dd_data = json.loads(zlib.decompress(request.data))
      for d in dd_data:
        check_to_point(d)

  # handle /api/v1/series/ metrics
  elif 'series' in request.path:
    # metrics that are not encoded, usually means json
    if request.content_encoding == None:
      pass
      # haven't seen any yet
      #print("series")
      # print("json data")
      # dd_data = request.get_json()
      # dd_data = dd_data[0]
      # print(dd_data)

    # metrics that are zlib compressed
    elif request.content_encoding == 'deflate':
      dd_data = json.loads(zlib.decompress(request.data))

      # handle objects that begin with 'series'
      if 'series' in dd_data:
        series = dd_data['series']

        #d = series[0]
        for item in dd_data['series']:
          series_item_to_point(item)

    # if there's another compressed payload besides the one beginning with 'series'
    # then dump it out
    else:
      print("nope")
      print(dd_data)

  # handle /intake/ metrics
  elif 'intake' in request.path:
    pass
    # the /intake endpoint is a legacy one and based on the data sent to it, as seen
    # in https://github.com/DataDog/dd-agent/blob/master/tests/core/fixtures/payloads/legacy_payload.json
    # I don't think we need to do anything with this data
    # if request.content_encoding == 'deflate'
    #   print("intake")
    #   print("binary data")
    #   dd_data = json.loads(zlib.decompress(request.data))
    #   dd_data['processes'] == None
    #   for key, val in dd_data.items():
    #     if key == 'processes':
    #       print("skipping because its looong.")
    #     else:
    #       print("{} = {}".format(key, val))

  # finally, dump anything we haven't seen
  else:
    print("dunno")
    print(request.content_encoding)
    print(request.path)
    dd_data = json.loads(zlib.decompress(request.data))
    print("not sure")

def write_data(points):
  print(points)