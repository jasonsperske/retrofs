RetroFS-web
==========
A basic web server for accessing the local file system, accessable via a simple web interface.

How to use
---------

0. setup vEnv

```bash
python3 -m venv .
source ./bin/activate
```

1. Install the dependencies:

```bash
pip3 install -r requirements.txt
```

2. Run the server:

```bash
python3 retrofs-web.py [port=8080] [root_path=.]
```
