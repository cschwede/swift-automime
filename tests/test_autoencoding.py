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

import unittest

from swift.common.swob import Request

from autoencoding import middleware


class FakeApp(object):
    def __call__(self, env, start_response):
        start_response('200 OK', {})
        return []


class TestAutoEncoding(unittest.TestCase):

    def test_set_encoding(self):
        app = middleware.AutoEncodingMiddleware(FakeApp(), {})
        req = Request.blank('/v1/a/c/o.gz', environ={'REQUEST_METHOD': 'PUT'})
        res = req.get_response(app)
        self.assertEqual(res.environ['HTTP_CONTENT_ENCODING'], 'gzip')
        self.assertEqual(res.status_int, 200)


if __name__ == '__main__':
    unittest.main()
