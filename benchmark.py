#!/usr/bin/env python
from subprocess import Popen, PIPE

import httpx
import requests
import string
import timeit
import urllib3

class BenchmarkHTTP(object):
    """sequentially benchmarks across:
        1) microframeworks (Flask, Starlette)
        2) HTTP libraries (urllib3, requests, httpx)

        @param short: HTTP request is small JSON vs large TEXT
        @type  short: boolean
        @param cycles: number of HTTP requests per client
        @type  cycles: int
    """
    def __init__(self, short=True, cycles=1000):
        super(BenchmarkHTTP, self).__init__()
        # start flask server
        self.cycles = cycles
        self.short = short

    def benchmark(self):
        """entrypoint, starts Flask + Starlette"""

        # start microframeworks
        f = Popen('./flask_app.py')
        s = Popen('./starlette_app.py')
        try:
            flask_results = self._make_test(5555)
            starlette_results = self._make_test(5000)
        except Exception as e:
            pass
        finally:
            f.kill()
            s.kill()

        self._report_results(flask_results, starlette_results)

    def _append_urllib3(self):
        """gold standard"""
        dep_in = 'import urllib3; http_pool = urllib3.PoolManager()'
        self.tests.append((
            'urllib3', 
            dep_in,
            'body = http_pool.urlopen("GET", "$url").read()')
        )

    def _append_requests(self):
        """popular requests library, made with urllib3"""
        dep_in = 'import requests'
        self.tests.append((
            'requests', 
            dep_in, 
            'r = requests.get("$url", verify=True)')
        )

    def _append_httpx(self):
        """newer async oriented library, made from urllib3"""
        dep_in = 'import httpx;'
        self.tests.append((
            'httpx', 
            dep_in,
            'r = httpx.get("$url")')
        )

    def _make_test(self, port):
        """run tests on one microframework, return results"""
        self.tests = []
        results = []

        endpoint = 'ping' if self.short else 'pong'
        url = 'http://localhost:{}/{}'.format(
            port,
            endpoint)
        
        self._append_urllib3()
        self._append_requests()
        self._append_httpx()

        for test in self.tests:
            my_result = self._run_test(
                test[0],
                test[1],
                test[2],
                url,
                self.cycles
                )
            results.append((test[0], url, self.cycles, my_result[-1]))

        return results

    def _report_results(self, flask_results, starlette_results):
        """stdout"""
        print('- ' * 38)
        print('- ' * 17 + 'FLASK RESULTS' + ' -' * 16)
        print('_' * 75)
        print(flask_results)
        print('- ' * 38)
        print('- ' * 38)
        print('\n')
        print('- ' * 38)
        print('- ' * 15 + 'STARLETTE RESULTS' + ' -' * 14)
        print('_' * 75)
        print(starlette_results)
        print('- ' * 38)
        print('- ' * 38)
        print('\n')

    def _run_test(
        self,
        library,
        dependencies,
        executable,
        url, 
        cycles):
        """ Benchmarks start & end times comparing different HTTP libraries
            on different Python microframework libraries: Flask and Starlette
            
            @param library: name of the HTTP library
            @type  library: str
            @param dependencies: import library statement
            @type  dependencies: str
            @param executable: command to run
            @type  executable: str
            @param url: url of microframework under test
            @type  url: str
            @param cycles: num cycles, default 5000 cycles
            @type  cycles: str


            @return :results
            @rtype  :list
        """

        TIMER = timeit.default_timer
        print("START testing {0} performance with {1} cycles".format(library, cycles))

        command = string.Template(executable).substitute(url=url)
        benchmark = timeit.timeit(stmt=command, setup=dependencies, number=cycles, timer=TIMER)

        print("END testing result: {0}".format(benchmark))
        print(' ')
        
        return [library, cycles, benchmark]

    
if(__name__ == '__main__'):
    # larger request body benchmark
    BenchmarkHTTP(short=False).benchmark()
