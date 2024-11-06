from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json

class ChatHandler(SimpleHTTPRequestHandler):
    #edit to suit your needs
    base_folder = r'D:\Facebook server\your_facebook_activity\messages'

    def list_json_files(self):
        files = []
        for root_folder in ['archived_threads', 'inbox', 'e2ee_cutover']:
            subdir = os.path.join(self.base_folder, root_folder)
            for root, dirs, file_list in os.walk(subdir):
                for file in file_list:
                    #You might change this to "message_1.json"
                    if file == "messages.json":
                        relative_path = os.path.relpath(os.path.join(root, file), self.base_folder)
                        files.append(relative_path)
        return files

    def do_GET(self):
        if self.path == '/available_chats':
            files = self.list_json_files()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
        else:
            super().do_GET()

if __name__ == '__main__':
    PORT = 8000
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, ChatHandler)
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
