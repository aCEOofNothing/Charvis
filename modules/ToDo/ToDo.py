from msal import PublicClientApplication
import requests

CLIENT_ID = "e3dad347-9c9b-4fd4-9d83-2a3b202ec4c4"
AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = [
    "Tasks.Read"
]

app = PublicClientApplication(
    CLIENT_ID,
    authority=AUTHORITY
)

result = app.acquire_token_interactive(
    scopes=SCOPES
)

token = result["access_token"]

response = requests.get(
    "https://graph.microsoft.com/v1.0/me/todo/lists",
    headers={
        "Authorization": f"Bearer {token}"
    }
)

print(response.json())