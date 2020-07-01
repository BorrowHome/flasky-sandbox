# 监听本机的5000端口
bind = '0.0.0.0:5050'        #指定gunicorn的端口号

#preload_app = True

# 开启进程
workers=4
#workers = multiprocessing.cpu_count() * 2 + 1

# 每个进程的开启线程
#threads = multiprocessing.cpu_count() * 2

backlog = 2048

timeout = 60*60*10

# 工作模式为gevent
# worker_class = "gevent"

debug=True

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
daemon = True

# 进程名称
proc_name = 'gunicorn.pid'

# 进程pid记录文件
pidfile = 'app_pid.log'

loglevel = 'logs/debug'
logfile = 'logs/gun_debug.log'
accesslog = 'logs/gun_access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
errorlog = 'logs/gun_error.log'
