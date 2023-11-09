import base64

base64_message = 'ZHVsZWVrYS5yb3NoaW5pZUBheGlhdGFkaWdpdGFsbGFicy5jb206SVJPSW1kV3lHeE5QRHFBdVJmQlZCMkQ3'
base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')

print(message)