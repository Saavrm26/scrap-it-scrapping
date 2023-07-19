from rocket3 import Rocket3
import json
from subprocess import Popen, PIPE

def App(environ, start_response):
    print(environ)
    if environ["REQUEST_METHOD"] == "GET":
        start_response("200 OK", [("Content-Type", "text/html")])
        data = "<html><body>Healthy<body></html>"
        return [data]

    else:
        try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            request_body_size = 0
        try:
            request_body = environ["wsgi.input"].read(request_body_size)
            print(request_body)
            data = json.loads(request_body)
            print(data)
            location = data["location"]
            title = data["title"]

            try:
                indeed_command = " ".join(
                    [
                        "scrapy",
                        "crawl",
                        "indeed",
                        f'-a location="{location}"',
                        f'-a title="{title}"',
                    ]
                )
                p_indeed = Popen([indeed_command], stderr=PIPE, stdout=PIPE, shell=True)
                naukri_command = " ".join(
                    [
                        "scrapy",
                        "crawl",
                        "naukri",
                        f'-a location="{location}"',
                        f'-a title="{title}"',
                    ]
                )
                p_naukri = Popen([naukri_command], stderr=PIPE, stdout=PIPE, shell=True)

                stdout_i, stderr_i = p_indeed.communicate()
                print(stdout_i, stderr_i)
                stdout_n, stderr_n = p_naukri.communicate()
                print(stdout_n, stderr_n)
            except Exception as e:
                print(e)
                start_response("500", [])
                return ["Sorry try again later"]

            start_response("200 OK", [])
            return []
        except Exception as e:
            print(e)
            start_response("400 Bad Request", [])
            return []


server = Rocket3(("0.0.0.0", 8080), "wsgi", {"wsgi_app": App})
server.start()
