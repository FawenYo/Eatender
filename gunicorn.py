bind = "0.0.0.0:8001"
loglevel = "debug"
accesslog = "access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = "error.log"
workers = 4
threads = 4
reload = True