FROM aerokube/selenoid:1.9.0

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

ENTRYPOINT ["/usr/bin/selenoid", "-listen", ":4444", \
            "-container-network", "buykers_suppliers_backend", \
            "-conf", "/etc/selenoid/config/browsers.json", \
            "-video-output-dir", "/opt/selenoid/video/", \
            "-log-conf", "/etc/selenoid/config/container-logs.json", \
            "-service-startup-timeout", "60s", \
            "-session-attempt-timeout", "60s", \
            "-session-delete-timeout", "10s", \
            "-timeout", "60s", \
            "-limit", "2"]
