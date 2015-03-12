#This document explains how to use XMLRPC to control antinetcut service.

# Introduction #

XMLRPC is a way to do formal Remote Procedure Calls, it uses XML as the marshalling format and supported by many programming language in addition that it's platform independent.

XMLRPC server is bundled with antinetcut to allow developers to integrate their work with antinetcut, such as building Gnome Applet or any GUI interface to control antinetcut instead of using the command line interface.

# Example (Super Simple) #

I'll explain here how can you use xmlrpclib python module to bind and use antinetcut services.

```
import xmlrpclib

server = xmlrpclib.Server('http://localhost:46201')
```

Then you can call functions like server.stop() server.status() server.start() to stop, check if protection thread is running or not, and to start the protection thread if you stopped it via the stop() call.

Please note that upon starting the antinetcut daemon, the protection thread start automatically and when you stop the daemon, the XMLRPC server stops as well, so you won't be able to control it remotely anymore.

So you should start the daemon normally, but if you like to keep controlling remotely, you should stop/start using XMLRPC.