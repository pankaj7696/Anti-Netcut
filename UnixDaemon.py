import sys, os, time, atexit, logging
from signal import SIGTERM
class UnixDaemon:
        """
        A generic daemon class.
        Usage: subclass the Daemon class and override the run() method
        """

        def __init__(self, pidfile,name='UnixDaemon', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile
                self.name= name

                logger = logging.getLogger(name)
                handler = logging.FileHandler("/var/log/%s.log" % name)
                formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
                self.logger = logger

        def daemonize(self):
                """
                do the UNIX double-fork magic to fight zombies :)
                """
                try:
                    pid = os.fork()
                    if pid > 0:
                        # exit first parent
                        return
                        #sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
                # decouple from parent environment
                os.chdir("/")
                os.setsid()
                os.umask(0)
                # do second fork
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit from second parent
                                sys.exit(0)
                except OSError, e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)
                # redirect standard file descriptors
                sys.stdout.flush()
                sys.stderr.flush()
                si = file(self.stdin, 'r')
                so = file(self.stdout, 'a+')
                se = file(self.stderr, 'a+', 0)
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())
                # write pidfile
                atexit.register(self.delpid)
                pid = str(os.getpid())
                file(self.pidfile, 'w+').write("%s\n" % pid)
                self.run()
        def delpid(self):
                os.remove(self.pidfile)
        def start(self):
                """
                Start the daemon
                """
                # Check for a pidfile to see if the daemon already runs
                try:
                        pf = file(self.pidfile, 'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)
                # Start the daemon
                self.daemonize()

        def stop(self):
                """
                Stop the daemon
                """
                # Get the pid from the pidfile
                try:
                        pf = file(self.pidfile, 'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return # not an error in a restart
                # Try killing the daemon process       
                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError, err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print str(err)
                                sys.exit(1)
        def restart(self):
                """
                Restart the daemon
                """
                self.stop()
                self.start()
        def status(self):
                """
                Check for daemon status
                """
                try:
                        pf = file(self.pidfile, 'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None
                if not pid:
                        return False
                #send Signal (0) (Does nothing) and check if process is up or not
                try:
                    os.kill(pid, 0)
                except OSError, err:
                    return False
                return True
        def run(self):
                """
                Override this please
                """
                raise NotImplementedError