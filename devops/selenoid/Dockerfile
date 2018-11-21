FROM aerokube/selenoid:1.8.1

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

EXPOSE 4444

ENTRYPOINT ["/usr/bin/selenoid", "-listen", ":4444", "-conf", "/etc/selenoid/browsers.json", "-video-output-dir", "/opt/selenoid/video/"]
