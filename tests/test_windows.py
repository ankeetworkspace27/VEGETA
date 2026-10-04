from automation.window import window_controller


print()
print("==============================")
print("     VEGETA WINDOW TEST")
print("==============================")
print()

windows = window_controller.get_windows()

for window in windows:
    print(f"HWND: {window['hwnd']} | TITLE: {window['title']}")

print()
print(f"Total windows found: {len(windows)}")
print()
print("==============================")
print("       TEST COMPLETE")
print("==============================")