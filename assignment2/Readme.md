## An extension to Assignment 1                                                                                                                <https://github.com/Chaya16/CMPE273/tree/master/assignment1>

### Building another component for the assignment 1 expense management application to achieve the following:

- Dynamic Load Balancing
  - Implement a Router (round robin)

- Dynamic Replica Registration
  - A new component called Router will be implemented. As part of the node registration, whenever you launch the expense management application's Docker instance, it will auto-register to the own instance to the router.
    
- Failure Detection (via CircutBreaker)
  - Whenever a node reaches its CircuitBreaker's error count, the router should deregister the failed node from the routing table
    in Redis and forward the same request to the next available node.

#### Instructions:
- Start redis server, with the command "redis-server" (make sure redis is installed)
- Start all the instances of replicas you want "python app.py <Port#>"
- Start the proxy by "python proxy.py"
