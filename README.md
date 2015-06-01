# mc — a simple Mesos-DNS client


This is a simple [Mesos-DNS](http://mesosphere.github.io/mesos-dns/) client written in Python.

Use it as CLI tool like so:

    $ ./mc.py localhost redis.marathon.mesos
    $ Discovered redis.marathon.mesos running on 10.141.141.10:31000

Alternatively you can `import mc` in your Python app and use `lookup_service(mesosdns_server, service_name)` which will yield an `(ip, port)` tuple for the logical `service_name`.


