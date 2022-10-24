# Signal Server

This work is firstly inspired by [simple-signaling-server](https://www.100ms.live/blog/webrtc-python-react-app) and then further extended.

To run the application locally

```shell
make local-install
make local-run
```

To build and run as a docker container

```shell
make -i
```

To publish the docker image

```shell
docker login
make -i publish username=foo
```

to run the docker image on a server

```shell
docker run -d -p 8080:8080 --name signal-server username/signal-server:latest
```

> **_NOTE:_**  Open the firewall on the server