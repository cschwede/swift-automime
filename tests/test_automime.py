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

from automime import middleware


class FakeApp(object):
    def __call__(self, env, start_response):
        start_response('200 OK', {})
        return []


class FakeCache(object):

    def __init__(self, val):
        if 'status' not in val:
            val['status'] = 200
        self.val = val

    def get(self, *args):
        return self.val


class TestAutoEncoding(unittest.TestCase):
    def setUp(self):
        self.cache = FakeCache({'meta': {'automime': 'true'}})

    def test_set_type_only(self):
        app = middleware.AutoMimeMiddleware(FakeApp(), {})
        req = Request.blank(
            '/v1/a/c/obj.txt', environ={
                'REQUEST_METHOD': 'PUT', 'swift.cache': self.cache})
        res = req.get_response(app)
        self.assertEqual(res.environ.get('HTTP_CONTENT_TYPE'), 'text/plain')
        self.assertFalse(res.environ.get('HTTP_CONTENT_ENCODING', False))
        self.assertEqual(res.status_int, 200)

    def test_set_type_and_encoding(self):
        app = middleware.AutoMimeMiddleware(FakeApp(), {})
        req = Request.blank(
            '/v1/a/c/obj.txt.gz', environ={
                'REQUEST_METHOD': 'PUT', 'swift.cache': self.cache})
        res = req.get_response(app)
        self.assertEqual(res.environ.get('HTTP_CONTENT_TYPE'), 'text/plain')
        self.assertEqual(res.environ.get('HTTP_CONTENT_ENCODING'), 'gzip')
        self.assertEqual(res.status_int, 200)

    def test_unknown_type_encoding(self):
        app = middleware.AutoMimeMiddleware(FakeApp(), {})
        req = Request.blank(
            '/v1/a/c/obj.bla', environ={
                'REQUEST_METHOD': 'PUT', 'swift.cache': self.cache})
        res = req.get_response(app)
        self.assertFalse(res.environ.get('HTTP_CONTENT_TYPE', False))
        self.assertFalse(res.environ.get('HTTP_CONTENT_ENCODING', False))
        self.assertEqual(res.status_int, 200)

    def test_meta_not_set(self):
        app = middleware.AutoMimeMiddleware(FakeApp(), {})
        req = Request.blank(
            '/v1/a/c/obj.txt', environ={
                'REQUEST_METHOD': 'PUT',
                'swift.cache': FakeCache({'meta': {}})})

        res = req.get_response(app)
        self.assertEqual(res.environ.get('HTTP_CONTENT_TYPE'), None)
        self.assertFalse(res.environ.get('HTTP_CONTENT_ENCODING', None))
        self.assertEqual(res.status_int, 200)

    def test_env_cleared(self):
        app = middleware.AutoMimeMiddleware(FakeApp(), {})
        req = Request.blank('/v1/a/c/obj.txt',
                            environ={'REQUEST_METHOD': 'PUT',
                                     'CONTENT_TYPE': 'something'})
        res = req.get_response(app)
        self.assertEqual(res.environ.get('CONTENT_TYPE'), None)
        self.assertEqual(res.status_int, 200)


if __name__ == '__main__':
    unittest.main()
