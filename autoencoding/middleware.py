# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import mimetypes
import os

from swift.common.swob import Request
from swift.common.utils import register_swift_info

mimetypes.init()


class AutoEncodingMiddleware(object):

    def __init__(self, app, conf, *args, **kwargs):
        self.app = app

    def __call__(self, env, start_response):

        request = Request(env.copy())
        if request.method == "PUT":
            _, ext = os.path.splitext(request.path)
            encoding = mimetypes.encodings_map.get(ext)
            if encoding:
                env['HTTP_CONTENT_ENCODING'] = encoding

        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)
    register_swift_info('AutoEncoding')

    def auth_filter(app):
        return AutoEncodingMiddleware(app, conf)
    return auth_filter
