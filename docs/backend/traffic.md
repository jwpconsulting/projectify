<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Traffic control testing

We want to be able to test Projectify under various network conditions, such as
unreliable or slow TCP connections, where

- packets arrive too late (latency)
- packets are transmitted slowly (throughput)
- connections are interrupted
- connections fail to be established
- packets are dropped

Testing properties of the browser or OS network stack is out of scope here, so
we assume that a corrupted packet is considered dropped from the perspective of
our app.

# Traffic control with tc

In local development, the Projectify backend is accessed on the primary loop
back interface, meaning localhost / 127.0.0.1.

If we develop using the frontend proxy, the flow of packets from browser to the
backend is

1. The browser loads a page, let that page be the dashboard, and requests that
   page and all its resources from the Vite dev server
2. The Vite dev server sends the page and its resources back to the browser.
3. The page contents get loaded, parsed and the Svelte Kit application boots
   up, and fires off several fetch requests for Projectify resources such as
   workspace, or current user, to the Vite dev server.
4. The Vite dev server proxies that request the the Django backend
5. The Django backend does its thing, connects to the database, and returns
   data to the Vite dev server
6. The Vite dev server, upon receiving this, forwards the data to the browser
7. The browser receives the fetch response, hands it over to the SvelteKit app,
   and page content is rendered.

With traffic control, we are interested in two of the above steps, 4. and 5.
Namely, the steps where the backend receives and transmits HTTP data. The
Django backend communicates through the loopback interface, and we can use tc
to shape ingress and egress traffic.

# Environment

We are on

- Debian 12 (bookworm), with
- Linux 6.1.0-18-amd64. We use
- iproute2-6.1.0,
- libbpf 1.1.0 (`tc -V`), and
- httperf-0.9.1.

# Httperf

We use Httperf to measure latency from the terminal, and establish the
following base values on the development workstation:

```
httperf --hog --server localhost --port 3000 --num-conn 1000
httperf --hog --server localhost --port 8000 --num-conn 1000
```

For the Vite dev server, we have

```
httperf --hog --client=0/1 --server=localhost --port=3000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=1000 --num-calls=1
Maximum connect burst length: 1

Total: connections 1000 requests 1000 replies 1000 test-duration 10.739 s

Connection rate: 93.1 conn/s (10.7 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 9.2 avg 10.7 max 26.9 median 10.5 stddev 2.4
Connection time [ms]: connect 0.4
Connection length [replies/conn]: 1.000

Request rate: 93.1 req/s (10.7 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 92.2 avg 93.4 max 94.6 stddev 1.7 (2 samples)
Reply time [ms]: response 10.3 transfer 0.0
Reply size [B]: header 300.0 content 78230.0 footer 0.0 (total 78530.0)
Reply status: 1xx=0 2xx=1000 3xx=0 4xx=0 5xx=0

CPU time [s]: user 2.72 system 8.02 (user 25.3% system 74.7% total 100.0%)
Net I/O: 7146.8 KB/s (58.5*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

For Django, we have

```
httperf --hog --client=0/1 --server=localhost --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=1000 --num-calls=1
Maximum connect burst length: 1

Total: connections 1000 requests 1000 replies 1000 test-duration 12.581 s

Connection rate: 79.5 conn/s (12.6 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 11.7 avg 12.6 max 63.5 median 12.5 stddev 2.8
Connection time [ms]: connect 0.2
Connection length [replies/conn]: 1.000

Request rate: 79.5 req/s (12.6 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 79.6 avg 79.6 max 79.6 stddev 0.0 (2 samples)
Reply time [ms]: response 12.3 transfer 0.1
Reply size [B]: header 616.0 content 130667.0 footer 0.0 (total 131283.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=1000 5xx=0

CPU time [s]: user 3.32 system 9.26 (user 26.4% system 73.6% total 100.0%)
Net I/O: 10195.6 KB/s (83.5*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

One being faster (Net I/O) than the other here is irrelevant, since the `/`
paths server different functions.

# Latency emulation

To introduce latency, we can add a constant delay to packets using `tc qdisc`
(queuing discipline). We choose for the delay to be 1000 ms and run the
following command to set up traffic control:

```bash
sudo tc qdisc add dev lo root netem delay 1000ms
```

We can verify that the qdisc setting is in effect, first by display it like so:

```bash
sudo tc qdisc show dev lo
```

This gives us:

```
qdisc netem 8001: root refcnt 2 limit 1000 delay 1s
```

For the backend, we can confirm that it is **very** slow, as a matter of fact,
we had to limit to `--num-conn 5` to get httperf to finish in time. Note that
Httperf executes connections sequentially, and not in parallel.

```
httperf --hog --client=0/1 --server=localhost --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=5 --num-calls=1
Maximum connect burst length: 1

Total: connections 5 requests 5 replies 5 test-duration 100.107 s

Connection rate: 0.0 conn/s (20021.5 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 20014.6 avg 20021.5 max 20047.4 median 20014.5 stddev 14.5
Connection time [ms]: connect 2003.9
Connection length [replies/conn]: 1.000

Request rate: 0.0 req/s (20021.5 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.2 stddev 0.1 (20 samples)
Reply time [ms]: response 2017.4 transfer 16000.2
Reply size [B]: header 624.0 content 130615.0 footer 0.0 (total 131239.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=5 5xx=0

CPU time [s]: user 25.52 system 74.58 (user 25.5% system 74.5% total 100.0%)
Net I/O: 6.4 KB/s (0.1*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

There is a significant slow down, despite bandwidth not being limited.

We can remove the configuration using the following command:

```bash
sudo tc qdisc del dev lo root
```

And we verify there are no more qdisc settings using the following:

```bash
sudo tc qdisc show dev lo
```

After which we see this:

```
qdisc noqueue 0: root refcnt 2
```

# Throughput emulation

To simulate a low packet throughput we use a _Token Bucket Filter_. We can use
the following invocation to set it up:

```bash
# Slow Modem
# You can use sudo tc qdisc change instead if qdisc already set up
sudo tc qdisc add dev lo root netem rate 56kbit
# T1 speed
sudo tc qdisc change dev lo root netem rate 1.544mbit
```

We time the requests to Django on port 8000 again:

```
httperf --hog --client=0/1 --server=localhost --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=5 --num-calls=1
Maximum connect burst length: 1

Total: connections 5 requests 5 replies 5 test-duration 99.776 s

Connection rate: 0.1 conn/s (19955.3 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 19486.9 avg 19955.3 max 21025.2 median 19613.5 stddev 643.9
Connection time [ms]: connect 70.6
Connection length [replies/conn]: 1.000

Request rate: 0.1 req/s (19955.3 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.2 stddev 0.1 (19 samples)
Reply time [ms]: response 1255.7 transfer 18629.0
Reply size [B]: header 614.0 content 130625.0 footer 0.0 (total 131239.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=5 5xx=0

CPU time [s]: user 25.90 system 73.87 (user 26.0% system 74.0% total 100.0%)
Net I/O: 6.4 KB/s (0.1*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

While monitoring the request, we see that it slows down to a trickle, but no
significant latency is observable. The average connection time is at 70.6. With
the latency limited, average connection time was 2003.9 ms.

For T1, we measure

```
httperf --hog --client=0/1 --server=localhost --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=5 --num-calls=1
Maximum connect burst length: 1

Total: connections 5 requests 5 replies 5 test-duration 3.541 s

Connection rate: 1.4 conn/s (708.2 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 707.4 avg 708.2 max 708.8 median 708.5 stddev 0.5
Connection time [ms]: connect 1.8
Connection length [replies/conn]: 1.000

Request rate: 1.4 req/s (708.2 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.0 stddev 0.0 (0 samples)
Reply time [ms]: response 57.5 transfer 648.8
Reply size [B]: header 618.0 content 130624.0 footer 0.0 (total 131242.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=5 5xx=0

CPU time [s]: user 0.82 system 2.72 (user 23.0% system 77.0% total 100.0%)
Net I/O: 181.1 KB/s (1.5*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

One major factor in sequential packet transmission, e.g. TCP, is that even
_mild_ bandwidth limitations, like T1-like speed, can severely influence total
duration required to serve requests.

We remove the qdisc setting again:

```
sudo tc qdisc del dev lo root
```

# Packet loss

Now, to introduce a packet loss of 15% (Bernoulli distribution), we can
configure the queuing discipline like so:

```bash
sudo tc qdisc add dev lo root netem loss random 15%
```

We time the requests to TCP port 8000 again.

```
httperf --hog --client=0/1 --server=localhost --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=5 --num-calls=1
Maximum connect burst length: 1

Total: connections 5 requests 5 replies 5 test-duration 4.449 s

Connection rate: 1.1 conn/s (889.8 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 14.0 avg 889.8 max 3135.0 median 435.5 stddev 1276.4
Connection time [ms]: connect 206.4
Connection length [replies/conn]: 1.000

Request rate: 1.1 req/s (889.8 ms/req)
Request size [B]: 62.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.0 stddev 0.0 (0 samples)
Reply time [ms]: response 55.5 transfer 627.9
Reply size [B]: header 612.0 content 130624.0 footer 0.0 (total 131236.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=5 5xx=0

CPU time [s]: user 1.26 system 3.19 (user 28.2% system 71.8% total 100.0%)
Net I/O: 144.1 KB/s (1.2*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

Again, we observe that packet loss influences Net I/O significantly.

# Applying qdisc based on port

Finally, we would like to only restrict port 8000, where the Django application
lives. For this, we need to host the Django application from a different
virtual interface. Researching this topic and finding
[this ArchWiki article on this topic](https://wiki.archlinux.org/title/Advanced_traffic_control#Using_tc_only),
I concluded that iptables or tc-u32 filtering will be too fiddly, since
loopback is not an Ethernet interface with the full packet stack available.

We create a virtual network interface pair `djangoserve` and `djangolisten`.
Django will listen on `djangolisten`, and we will connect to `djangolisten`
from the Vite dev server:

```bash
# Listen on djangolisten
# Connect to djangoserve
sudo ip link add djangoserve type veth peer name djangolisten
```

We create a namespace for Django:

```bash
# Put djangolisten in a separate namespace
sudo ip netns add django
sudo ip link set djangolisten netns django
```

And we assign ip addresses to both interfaces:

```bash
# Assign addresses to each veth if
sudo ip addr add 192.168.128.10/24 dev djangoserve
sudo ip netns exec django ip addr add 192.168.128.1/24 dev djangolisten
```

We make sure the devices are up:

```bash
# Set both devices up
sudo ip link set djangoserve up
sudo ip netns exec django ip link set djangolisten up
sudo ip netns exec django ip link set lo up
```

We can test the route works:

```
# ping -c1 192.168.128.1
PING 192.168.128.1 (192.168.128.1) 56(84) bytes of data.
64 bytes from 192.168.128.1: icmp_seq=1 ttl=64 time=0.100 ms

--- 192.168.128.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.100/0.100/0.100/0.000 ms
```

# Running Django in the namespace

To ensure that Django can connect to the database even from within a namespace,
I configure the DATABASE_URL to be

```
DATABASE_URL = postgres://%2Fvar%2Frun%2Fpostgresql/projectify
```

For the backend, we insert into `.env` the `ALLOWED_HOSTS` config:

```
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.128.1
```

We have to run Django from the same ip namespace:

```fish
sudo ip netns exec django sudo --user $USER -- \
  (which fish) -c "poetry run ./manage.py runserver 192.168.128.1:8000"
```

We can now try httperf:

```
httperf --hog --client=0/1 --server=192.168.128.1 --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=5 --num-calls=1
Maximum connect burst length: 1

Total: connections 5 requests 5 replies 5 test-duration 0.375 s

Connection rate: 13.3 conn/s (75.0 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 48.4 avg 75.0 max 82.0 median 81.5 stddev 14.8
Connection time [ms]: connect 33.5
Connection length [replies/conn]: 1.000

Request rate: 13.3 req/s (75.0 ms/req)
Request size [B]: 66.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.0 stddev 0.0 (0 samples)
Reply time [ms]: response 41.4 transfer 0.0
Reply size [B]: header 262.0 content 2731.0 footer 0.0 (total 2993.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=5 5xx=0

CPU time [s]: user 0.06 system 0.31 (user 17.0% system 83.0% total 100.0%)
Net I/O: 39.8 KB/s (0.3*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

Now comes the exciting part where we apply a queue discipline:

```bash
sudo tc qdisc add dev djangoserve root netem rate 56kbit
sudo ip netns exec django sudo tc qdisc add dev djangolisten root netem rate 56kbit
```

Httperf gives us:

```
httperf --hog --client=0/1 --server=192.168.128.1 --port=8000 --uri=/ --send-buffer=4096 --recv-buffer=16384 --ssl-protocol=auto --num-conns=5 --num-calls=1
Maximum connect burst length: 1

Total: connections 5 requests 5 replies 5 test-duration 2.652 s

Connection rate: 1.9 conn/s (530.4 ms/conn, <=1 concurrent connections)
Connection time [ms]: min 516.4 avg 530.4 max 533.9 median 533.5 stddev 7.8
Connection time [ms]: connect 36.6
Connection length [replies/conn]: 1.000

Request rate: 1.9 req/s (530.4 ms/req)
Request size [B]: 66.0

Reply rate [replies/s]: min 0.0 avg 0.0 max 0.0 stddev 0.0 (0 samples)
Reply time [ms]: response 470.4 transfer 23.3
Reply size [B]: header 262.0 content 2731.0 footer 0.0 (total 2993.0)
Reply status: 1xx=0 2xx=0 3xx=0 4xx=5 5xx=0

CPU time [s]: user 0.68 system 1.97 (user 25.8% system 74.2% total 100.0%)
Net I/O: 5.6 KB/s (0.0*10^6 bps)

Errors: total 0 client-timo 0 socket-timo 0 connrefused 0 connreset 0
Errors: fd-unavail 0 addrunavail 0 ftab-full 0 other 0
```

Now, we can point the frontend to connect to our new backend and set the `.env`
file to be:

```
VITE_USE_LOCAL_PROXY=
VITE_WS_ENDPOINT=/ws
VITE_API_ENDPOINT=/api
VITE_PROXY_WS_ENDPOINT=ws://192.168.128.1:8000/ws
VITE_PROXY_API_ENDPOINT=http://192.168.128.1:8000
```

# Adjustments and cleanup

If we want to adjust the speed, we just run:

```fish
begin
  set -l speed 32kbit
  set -l latency 100ms
  sudo tc qdisc change dev djangoserve root netem rate $speed latency $latency
  sudo ip netns exec django sudo tc qdisc change dev djangolisten root netem rate $speed latency $latency
end
```

Did we, in a sense, re-invent what Podman/Docker can do? Perhaps. But also,
it's nice to be able to know how the traffic shaping works, and be able to make
adjustments to it by yourself.

For cleanup, we run

```
sudo tc qdisc del dev djangoserve root
sudo ip link del djangoserve
sudo ip netns del django
```

Now, the actual testing within the browser can start.

# Further information

- [tc man page](https://www.linux.org/docs/man8/tc.html)
- [tc Network Emulator syntax](https://www.linux.org/docs/man8/tc-netem.html)
- [tc universal 32bit traffic control filter](https://man7.org/linux/man-pages/man8/tc-u32.8.html)
- [ArchWiki on tc](https://wiki.archlinux.org/title/Advanced_traffic_control)
- [General tutorial on netbeez](https://netbeez.net/blog/how-to-use-the-linux-traffic-control/)
