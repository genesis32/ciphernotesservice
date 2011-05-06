
import urlparse

def get_http_post_params(params):
   res = {}
   for v in urlparse.parse_qsl(params):
        res[v[0]] = v[1]
   return res
