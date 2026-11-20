
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import time


notes: list = []
next_id: int = 1


class NotesHandler(BaseHTTPRequestHandler):
  
    def handle_one_request(self) -> None:

        self.start_time: float = time.perf_counter()

        super().handle_one_request()

    def log_request(self, code: int = 200, size: int = -1) -> None:

        end_time: float = time.perf_counter()

        time_taken: float = (end_time - self.start_time) * 1000

        print(
            f"{self.command} {self.path} | "
            f"Status: {code} | "
            f"Time: {time_taken:.2f} ms"
        )


    
 
    def do_GET(self) -> None:

        if self.path == "/notes":

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps(notes)
            self.wfile.write(response.encode("utf-8"))

        elif self.path.startswith("/notes/"):

            note_id: str = self.path.split("/")[-1]

            if note_id.isdigit():

                for note in notes:

                    if note["id"] == int(note_id):

                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()

                        response: str = json.dumps(note)
                        self.wfile.write(response.encode("utf-8"))
                        return

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps({
                "error": f"Note {note_id} not found"
            })

            self.wfile.write(response.encode("utf-8"))

        else:

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps({
                "error": "Endpoint not found"
            })

            self.wfile.write(response.encode("utf-8"))


    def do_POST(self) -> None:
        global next_id

        if self.path == "/notes":

            content_length: int = int(
                self.headers.get("Content-Length", 0)
            )

            post_data: bytes = self.rfile.read(content_length)

            try:
                data: dict = json.loads(post_data)

            except (json.JSONDecodeError, UnicodeDecodeError):

                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response: str = json.dumps({
                    "error": "Invalid JSON"
                })

                self.wfile.write(response.encode("utf-8"))
                return

            if (
                not isinstance(data, dict)
                or not isinstance(data.get("text"), str)
                or not data["text"].strip()
            ):

                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response: str = json.dumps({
                    "error": "Valid note text is required"
                })

                self.wfile.write(response.encode("utf-8"))
                return

            note_id: int = next_id
            next_id += 1

            note: dict = {
                "id": note_id,
                "text": data["text"]
            }

            notes.append(note)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps(note)
            self.wfile.write(response.encode("utf-8"))

        else:

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps({
                "error": "Endpoint not found"
            })

            self.wfile.write(response.encode("utf-8"))
    
    def do_DELETE(self) -> None:

        if self.path.startswith("/notes/"):

            note_id: str = self.path.split("/")[-1]

            if note_id.isdigit():

                for note in notes:

                    if note["id"] == int(note_id):

                        notes.remove(note)

                        self.send_response(204)
                        self.end_headers()
                        return

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps({
                "error": "Note not found"
            })

            self.wfile.write(response.encode("utf-8"))

        else:

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            response: str = json.dumps({
                "error": "Endpoint not found"
            })

            self.wfile.write(response.encode("utf-8"))
    
    def method_not_allowed(self) -> None:

        self.send_response(405)
        self.send_header("Content-Type", "application/json")
        self.send_header("Allow", "GET, POST, DELETE")
        self.end_headers()

        response: str = json.dumps({
            "error": "Method not allowed"
        })

        self.wfile.write(response.encode("utf-8"))

    def do_PUT(self) -> None:
        self.method_not_allowed()

    def do_PATCH(self) -> None:
        self.method_not_allowed()



def main() -> None:

    server: HTTPServer = HTTPServer(
        ("localhost", 8080),
        NotesHandler
    )

    print("Server running at http://localhost:8080")

    server.serve_forever()


if __name__ == "__main__":
    main()
