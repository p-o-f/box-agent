import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from box_sdk_gen import BoxClient, BoxOAuth, OAuthConfig, GetAuthorizeUrlOptions

load_dotenv()

CLIENT_ID = os.getenv("BOX_CLIENT_ID")
CLIENT_SECRET = os.getenv("BOX_CLIENT_SECRET")

auth_code_holder = {}

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if "code" in params:
            auth_code_holder["code"] = params["code"][0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Auth complete! You can close this tab.")
    def log_message(self, format, *args):
        pass

oauth_config = OAuthConfig(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
oauth = BoxOAuth(config=oauth_config)
options = GetAuthorizeUrlOptions(redirect_uri="http://localhost:8080/callback", response_type="code")
auth_url = oauth.get_authorize_url(options=options)
print("Opening browser for Box login...")
webbrowser.open(auth_url)

server = HTTPServer(("localhost", 8080), CallbackHandler)
server.handle_request()
oauth.get_tokens_authorization_code_grant(authorization_code=auth_code_holder["code"])

client = BoxClient(auth=oauth)

# List root folders first
print("\n📁 Your Box root folders:")
items = client.folders.get_folder_items("0")
for item in items.entries:
    print(f"  [{item.type}] {item.name} (id: {item.id})")