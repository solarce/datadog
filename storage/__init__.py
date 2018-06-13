# # configuration
# if 'wf_host' not in agent_config:
#   log.error('Agent config missing wf_host (the Wavefront proxy host)')
#   return
# proxy_host = agent_config['wf_host']
# if 'wf_port' in agent_config:
#   proxy_port = int(agent_config['wf_port'])
# else:
#   proxy_port = 2878
# self.proxy_dry_run = ('wf_dry_run' in agent_config and
#                       (agent_config['wf_dry_run'] == 'yes' or
#                        agent_config['wf_dry_run'] == 'true'))
# if log:
#   log.debug('Wavefront Emitter %s:%d ', proxy_host, proxy_port)
#
# if 'wf_meta_tags' in agent_config:
#   self.meta_tags = [tag.strip() for tag in
#                     agent_config['wf_meta_tags'].split(',')]
#
# try:
#   # connect to the proxy
#   if not self.proxy_dry_run:
#     self.sock = socket.socket()
#     self.sock.settimeout(10.0)
#     try:
#       self.sock.connect((proxy_host, proxy_port))
#     except socket.error as sock_err:
#       err_str = (
#           'Wavefront Emitter: Unable to connect %s:%d: %s' %
#           (proxy_host, proxy_port, str(sock_err)))
#       if log:
#         log.error(err_str)
#       else:
#         print err_str
#       return
#   else:
#     self.sock = None