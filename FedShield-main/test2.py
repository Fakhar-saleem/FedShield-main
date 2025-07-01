# # from client_login import start_client, register_client

# # # Establish the SSL connection to the server
# # start_client()

# # # Now proceed with registration
# # reg_message = "register_user@DLP@124@DLP@newuser2@DLP@secret123"
# # register_client(reg_message)
# import os

# # After login, launch the main DLP system
# os.system("python admin_window.py")

from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

response = client.chat.completions.create(
    model="deepseek-ai/deepseek-r1",
    messages=[{"role": "user", "content": "Hello, how are you?"}],
    max_tokens=100
)

print(response)
