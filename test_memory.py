import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load secrets from your .env file
load_dotenv()

api_key = os.getenv("HINDSIGHT_API_KEY")
bank_id = os.getenv("HINDSIGHT_BANK_ID")

print("Connecting to Hindsight...")
client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=api_key
)

# 1. Save a ticket to persistent memory
print(f"Storing memory into bank: {bank_id}...")
client.retain(
    bank_id=bank_id,
    content="Customer Alex (alex@acmecorp.com) uses Ubuntu 24.04. Reported issue: Docker port 5432 blocked by ufw firewall. Prefers direct bash commands without boilerplate."
)
print("Memory saved successfully!")

# 2. Recall that memory
print("\nRecalling memory...")
memories = client.recall(
    bank_id=bank_id,
    query="What OS and issues does Alex have?"
)

print("\nRecalled Memories from Hindsight:")
for mem in memories.results:
    print(f"- {mem.text}")