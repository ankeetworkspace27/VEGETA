import time

from automation.search import search_manager


print()
print("==============================")
print("     VEGETA SEARCH TEST")
print("==============================")

print()
print("Setting target to YouTube...")

search_manager.set_target("youtube")

print()
print("Target:", search_manager.get_target())

print()
print("Make sure Chrome is open.")
print("Starting search in 3 seconds...")

time.sleep(3)

result = search_manager.search("Python videos")

print()
print("Search result:", result)

print()
print("==============================")
print("       TEST COMPLETE")
print("==============================")