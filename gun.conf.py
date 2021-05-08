import multiprocessing
wsgi_app="new_wuhu/"

chdir="new_wuhu/"

bind = "172.22.185.194:8000"

timeout=30

works = multiprocessing.cpu_count() * 2 + 1

threads = multiprocessing.cpu_count() * 2

max_requests = 2000   #worker重启之前处理的最大requests数， 缺省值为0表示自动重启disabled。主要是防止内存泄露。

graceful_timeout = 20  #接收到restart信号后，worker可以在graceful_timeout时间内，继续处理完当前requests。

work_class = "gevent"

access_log = "new_wuhu/Log/wuhu_gunicorn/access.log"

error_log = "nwe_wuhu/Log/wuhu_gunicorn/error.log"
