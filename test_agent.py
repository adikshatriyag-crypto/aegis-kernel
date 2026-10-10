from aegis import AegisShield, SecurityViolationException

# 1. Initialize the Aegis Shield
shield = AegisShield()

# 2. A developer's regular agent tool wrapped with Aegis Shield
@shield.protect_tool
def read_system_file(file_path: str, is_tainted: bool = True):
    return f"Contents of {file_path}: [SUPER DUPER SECRET DATA]"

print("\n" + "=" * 65)
print("🤖 ENTERPRISE AI AGENT WITH AEGIS SHIELD ATTACHED")
print("=" * 65)

# TEST 1: Normal Safe Action
print("\n[TEST 1] User asks to read safe public file:")
try:
    result = read_system_file("C:/public/welcome.txt", is_tainted=False)
    print(f"✅ Success: {result}")
except SecurityViolationException as e:
    print(e)

# TEST 2: Hacker tries prompt injection to read database keys
print("\n[TEST 2] Hacker injects payload to steal .env credentials:")
try:
    result = read_system_file("C:/app/.env", is_tainted=True)
    print(f"❌ LEAKED: {result}")
except SecurityViolationException as e:
    print(f"🛡️  PROTECTED: Threat neutralized successfully!")
    print(e)

print("=" * 65 + "\n")