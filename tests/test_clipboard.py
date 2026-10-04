from automation.clipboard import clipboard_manager


print()
print("==============================")
print("   VEGETA CLIPBOARD TEST")
print("==============================")
print()

# ---------------------------------------------------------
# 1. SET
# ---------------------------------------------------------

print("1. Setting clipboard...")

result = clipboard_manager.set_text(
    "VEGETA Phase 8 Clipboard Test"
)

print("Set result:", result)


# ---------------------------------------------------------
# 2. READ
# ---------------------------------------------------------

print()
print("2. Reading clipboard...")

text = clipboard_manager.get_text()

print("Clipboard contents:", text)


# ---------------------------------------------------------
# 3. CLEAR
# ---------------------------------------------------------

print()
print("3. Clearing clipboard...")

result = clipboard_manager.clear()

print("Clear result:", result)


# ---------------------------------------------------------
# 4. VERIFY
# ---------------------------------------------------------

print()
print("4. Reading clipboard after clearing...")

text = clipboard_manager.get_text()

print("Clipboard contents:", repr(text))


# ---------------------------------------------------------
# COMPLETE
# ---------------------------------------------------------

print()
print("==============================")
print("       TEST COMPLETE")
print("==============================")