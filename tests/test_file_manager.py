from automation.file_manager import file_manager


print()
print("==============================")
print("   VEGETA FILE MANAGER TEST")
print("==============================")
print()

home = file_manager.expand_path("~")
print("Home directory:")
print(home)

print()
print("Desktop path:")
print(file_manager.expand_path("~/Desktop"))

print()
print("Creating test folder...")

test_folder = file_manager.expand_path(
    "~/VEGETA_PHASE8_TEST"
)

result = file_manager.create_folder(test_folder)

print()
print("Create folder result:", result)

print()
print("Listing home directory...")

items = file_manager.list_directory("~")

print("Items found:", len(items))

for item in items[:10]:
    print(
        f"{item['type'].upper():6} | "
        f"{item['name']}"
    )

print()
print("Finding the test folder...")

results = file_manager.find(
    "VEGETA_PHASE8_TEST",
    "~"
)

for result in results:
    print(result)

print()
print("==============================")
print("       TEST COMPLETE")
print("==============================")
