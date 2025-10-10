# revil
Revil is a pentesting suite for the Berkeley r-commands. The r-commmands are inherently insecure because they put to much trust into the client sending things like username or hostname / ip. Thus it can be a good target for pentesters.

# Work in Progress
Although the first couple of functionalities are working like rlogin and potentially rsh, the suite is still in a heavy work in progress phase.

# Motivation
When I was solving a hackthebox machine which needed to exploit rlogins trust feature I found that the normal `rlogin` does not allow to spoof your original username. I needed to make a new user with the correct name and use it to login. Revil eliminates this problem by allowing to spoof usernames and (eventually) IPs

# Usage
Programm needs to run as root to work because the r-commands sometimes require the client to establish a connection FROM a restricted (< 1024) port.
```shell
revil --help # For now see this for usage
```
