### Application Layer (Layer - 7) Load Balancer
 

Application layer involves the application protocols - it may mean http, https, resp. 
Application load balancer means that it'll will get an incoming request on one of the protocol that it supports. Then forwards (copy and sends new request) to the other server on a different/same protocol 

So with this load balancer, we can update headers, read the url and based on that do that routing. We have the request body as well, but its not parsed for the sake of efficiency.

It support https, https1.1


### Transport Layer (Layer - 4) Load Balancer

Layer 4 just forwards the network packets to servers configured. 
So it makes two socket connections - one with downstream and one with upstream. Any data recieved from one side and forwarded to another side. 

This load balancer also support layer 4 load balancing.


### Configurations 


This load balancer has both layer-4 and layer-7 configurations. It reads the configurations from config.yaml 

TODO : 

* Layer-4 with fast api websocket only
* Add other load balancing algorithms (weighted and least connections - will need to have connection pool)
* Make .conf file feature (I'll just make it a yaml)
* Edit header feature in layer-7 
* Path based, header based routing in layer-7





