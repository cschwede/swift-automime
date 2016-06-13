Openstack Swift automime middleware
====================================================

``automime`` is a middleware that sets the content-encoding and content-type
metadata entry automatically by checking the object name suffix on PUT requests.
It is disabled by default and can be enabled on a per-container basis.

Quick Install
-------------

1) Install automime:

    git clone git://github.com/cschwede/swift-automime.git
    cd swift-automime
    sudo python setup.py install

2) Add a filter entry for automime to your proxy-server.conf:

    [filter:automime]
    use = egg:automime#automime

3) Alter your proxy-server.conf pipeline and add automime after any
   authentication middleware:

    [pipeline:main]
    pipeline = catch_errors healthcheck cache tempauth formpost tempurl automime proxy-server

4) Restart your proxy server:

    swift-init proxy reload

5) Enable this for a given container:

    swift post container -m "automime: true"

Done!
