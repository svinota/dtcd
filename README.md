dtc
===

Dynamic network blocks allocation via simple HTTP RPC

Usage::

    # allocate a network
    $ curl -X POST --data "$uuid" http://localhost:7623/v1/network/

    # free a previously allocated network
    $ curl -X DELETE --data "$uuid" http://localhost:7623/v1/network/

    # list current allocations
    $ curl http://localhost:7623/v1/network/ | python -m json.tool
