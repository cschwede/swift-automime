Openstack Swift auto-encoding middleware
====================================================

``autoencoding`` is a middleware that sets the content-encoding metadata entry
automatically by checking the object name suffix on PUT requests.

Quick Install
-------------

1) Install autoencoding:

    git clone git://github.com/cschwede/swift-autoencoding.git
    cd swift-autoencoding
    sudo python setup.py install

2) Add a filter entry for autoencoding to your proxy-server.conf:

    [filter:autoencoding]
    use = egg:autoencoding#autoencoding

3) Alter your proxy-server.conf pipeline and add autoencoding after any
   authentication middleware:

    [pipeline:main]
    pipeline = catch_errors healthcheck cache tempauth formpost tempurl autoencoding proxy-server

4) Restart your proxy server:

    swift-init proxy reload

Done!
