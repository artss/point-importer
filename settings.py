libs = ['/home/point/core/lib']

# redis
cache_socket = 'unix:///var/run/redis/cache.sock'
storage_socket = 'unix:///var/run/redis/storage.sock'

db = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'point',
    'user': 'point',
    'password': 'point',
    'maxsize': 10
}

cache_expire_max = 86400 * 7
ids_cache_expire = cache_expire_max

domain = 'point.im'

lang = 'en'
timezone = 'Europe/Moscow'

media_path = '/home/point/img/m'
media_root = '://i.point.im/m'

thumbnail_path = '/home/point/img/t'
thumbnail_root = '://i.point.im/t'
thumbnail_size = [400, 300]

imgproc_sock = '/tmp/imgproc.sock'
upload_dir = '/home/point/upload'

proctitle = 'point-importer'

logger = 'importer'
logfile = '/home/point/log/importer.log'
loglevel = 'info'
logrotate = None
logcount = 7

debug = False

secret = 'my secret phrase'

try:
    from settings_local import *
except ImportError:
    pass

