Kickass_Benchmarking
====================

steps forward:

client:
    pick size data chunk
    wait (rho time)
    sends
    [kickass: exponential times, pareto sizes]

implement sizes from 1) uniform (all random)
                     2) exponential
                     3) pareto



NEXT:
add a number of clients to congest the network
    Each draws from the same distribution, with different randomly selected parameters

multiprocessing library!
HTTP requests (GET, ACK, etc.) [there is a python library for this]
    client: sends request for a URL
    server: response: k bytes (not really important what it contains)

structure: keep application structure separate
1) bulk data - threading
2) http-esque

priorities
1) threading/multi-processing
2) HTTP-ish structure
3) TCP-level information (rate of how fast it was supposed to send at)


Data Reporting:
flow was N bytes long
log time every k bytes (charts throughput over time)
total bytes vs. time (visualize how smooth the flow is) [TCP Dump]
send 100 packets, record time, repeat
    if time - wireshark/tcp dump creates file called pcap which contains flow info
    

, threads library may be useful
    want NO GLOBAL PROCESSING LOCK


HTTP Traffic



Report:
Diagrams of what we're doing, how it works.