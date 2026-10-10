import time

print("\n" + "=" * 65)
print("🦹 MIT HACKER SIMULATION: TRYING TO BYPASS AEGIS")
print("=" * 65)

# Hacker Trick: Disguising the attack as a harmless text
sneaky_hacker_attack = {
    "action": "FILE_READ",
    # Hacker hides the intent in sub-paths
    "target": "C:/confidential/../confidential/company_secrets.env",
    "origin": "UNTRUSTED_EXTERNAL_WEBHOOK",
    "is_tainted": True
}

print(f"\n[!] Hacker attempts path-traversal bypass trick...")
print(f"    Payload: {sneaky_hacker_attack['target']}")

# AEGIS Dynamic Kernel Interceptor
def aegis_security_guard(tool_call):
    # Rule 1: Origin analysis
    if tool_call["is_tainted"]:
        # Rule 2: Invariant check (No tainted data can resolve to system files)
        forbidden_targets = [".env", "secret", "password", "key", "token"]
        target = tool_call["target"].lower()
        
        if any(f in target for f in forbidden_targets):
            return False, "BLOCKED: Taint violation on protected resource"
            
    return True, "ALLOWED"

# Execution
allowed, reason = aegis_security_guard(sneaky_hacker_attack)

print("\n" + "-" * 65)
if not allowed:
    print(f"🛡️  AEGIS VERDICT: {reason}")
    print("🎯  HACKER RESULT: FAILED! MIT/KGB attack neutralized completely.")
else:
    print("❌  SYSTEM VULNERABLE!")
print("-" * 65 + "\n")