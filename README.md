dtcd
====

Dynamic network blocks allocation via simple HTTP RPC

requirements
------------

* python
* netaddr

usage
-----

With curl::

    # allocate an IPv4 network
    $ curl -X POST --data "$uuid" http://localhost:7623/v1/network/ipv4/

    # free a previously allocated network
    $ curl -X DELETE --data "10.0.0.0/24" http://localhost:7623/v1/network/ipv4/

    # list current allocations
    $ curl http://localhost:7623/v1/network/ | python -m json.tool
