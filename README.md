<div align=center>
  <img height="150" src="https://raw.githubusercontent.com/hydr0nium/revil/refs/heads/main/assets/revil.svg" alt="" />
  <h1>revil</h1>
![python](https://img.shields.io/badge/Python-3.11%2B-blue)
</div>


`revil` is a pentesting suite for the Berkeley r-commands. The r-commmands are inherently insecure because they put to much trust into the client sending things like username or hostname / ip. Thus it can be a good target for pentesters.

> [!WARNING]
> This project is work in progress. The current version has some stable functions like rlogin and rsh but the stability is not guaranteed. 

# Installation
```shell
pipx install git+https://github.com/hydr0nium/revil.git
```
> [!TIP]
> To make revil globally available you can use the following commands
> ```shell
> sudo bash -c '$PATH' # To get the paths of root
> which revil # To get the path of revil
> sudo ln -s /path/to/revil/ /path/to/some/root/path
> ```

# Usage
`revil` may need to run as root because the r-commands often require the client to establish a connection from a privileged port.
> [!TIP]
> The root requirement can be disabled with the `--noroot` flag
```shell
usage: Revil [-h] {rlogin,rsh,rexec,rwho} ...

positional arguments:
  {rlogin,rsh,rexec,rwho}
    rlogin              Use rlogin
    rsh                 Use rsh
    rexec               Use rexec
    rwho                Use rwho

options:
  -h, --help            show this help message and exit
```
> [!IMPORTANT]
> The usage is subject to change

# 🗺️ Roadmap
- [x] username-spoofing
- [x] rlogin 
- [x] rsh 
- [ ] rexec
- [ ] rwho
- [ ] rstat
- [ ] rcp
- [ ] ruptime
- [ ] IP spoofing

# Motivation
> [!NOTE]
> When I was solving a hackthebox machine which needed to exploit rlogins trust feature I found that the normal `rlogin` does not allow to spoof your original username. I needed to make a new user with the correct name and use it to login. Revil eliminates this problem by allowing to spoof usernames and (eventually) IPs

