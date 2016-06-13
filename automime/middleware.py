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

from swift.common.http import is_success
from swift.common.swob import Request
from swift.common.utils import register_swift_info
from swift.proxy.controllers.base import get_container_info

mimetypes.init()


class AutoMimeMiddleware(object):

    def __init__(self, app, conf, *args, **kwargs):
        self.app = app

    def __call__(self, env, start_response):

        request = Request(env)
        if request.method == "PUT":
            # Ensure a possibly cached CONTENT_TYPE will be cleared
            if env.get('CONTENT_TYPE'):
                del env['CONTENT_TYPE']
            container_info = get_container_info(
                request.environ, self.app, swift_source='AM')
            if not container_info or not is_success(container_info['status']):
                return self.app(env, start_response)

            meta = container_info.get('meta', {})
            enabled = meta.get('automime')

            if not enabled:
                return self.app(env, start_response)

            _type, encoding = mimetypes.guess_type(request.path)
            if _type:
                env['HTTP_CONTENT_TYPE'] = _type
            if encoding:
                env['HTTP_CONTENT_ENCODING'] = encoding

        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)
    register_swift_info('automime')

    def auth_filter(app):
        return AutoMimeMiddleware(app, conf)
    return auth_filter
