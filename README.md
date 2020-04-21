# Flask and Starlette performance with urllib3, requests, and httpx

> published at https://aug2uag.blogspot.com/2020/04/network-load-performance-between.html

The purpose of this benchmark was to evaluate the performance difference under load for a Flask and Starlette microframework with various popular HTTP clients.

These benchmark results from 1000 cycles.

### Requirements

Developed and tested with Python 3.8

install dependencies and run `benchmark.py`


### Results

##### Flask @ 1000 cycles (testing smaller JSON response)
```
urllib3: 	6.009076181
requests: 	8.310135888
httpx:		14.922275728
```

##### Flask @ 1000 cycles (testing larger text response)
```
urllib3: 	6.489965677
requests: 	7.959935096000001
httpx:		15.216326602
```

##### Starlette @ 1000 cycles (testing smaller JSON response)
```
urllib3: 	6.489965677
requests: 	7.959935096000001
httpx:		15.216326602
```

##### Starlette @ 1000 cycles (testing larger text response)
```
urllib3: 	0.861392250999998
requests: 	7.092012402999998
httpx:		12.933335759999999
```


### Discussion

##### HTTP libraries

Across the board, the httpx library underperformed relative to requests and urllib3. This might be because the `httpx.get` method is not benefiting from its async capabilities. The most efficient library of the three was consistently urllib3, followed by the requests library.

The size difference in the request body in this experiment had little or no effect, and indicates the difference in the request bodies was nominal.

##### Frameworks

Both Flask and Starlette are similar in implementation. Flask is more focused on delivering a full-stack experience, while Starlette is organized to be more biased towards headless services.

The performance of Starlette was modestly more good relative to the requests library. However, Starlette was significantly more performant with urllib3.


### Discussion

The urllib3 results for Starlette may be indicating failure, although the server logs look Ok-- the performance of urllib3 with Starlette is simply unbelievable. Starlette and Python 3 are optimized with subroutines, which may explain the dramatic differences between Flask and Starlette in their performance with urllib3 in case it is working. In that case there are clear multithreading capabilities at work that are stratespherically advantageous to utilize in high performance network I/O applications written in Python. Whereas Flask utilizes WGSI, Starlette implements ASGI that seems to be on its way for taking over Python internet gateways.

Therefore, Starlette with ASGI has superior asynchronous performance relative to Flask.