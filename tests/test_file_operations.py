from automation.file_manager import file_manager


print()
print("==============================")
print(" VEGETA FILE OPERATIONS TEST")
print("==============================")
print()

# ---------------------------------------------------------
# TEST LOCATIONS
# ---------------------------------------------------------

test_folder = file_manager.expand_path(
    "~/VEGETA_PHASE8_TEST"
)

destination_folder = file_manager.expand_path(
    "~/VEGETA_PHASE8_TEST/Destination"
)

test_file = file_manager.expand_path(
    "~/VEGETA_PHASE8_TEST/test.txt"
)

renamed_file = file_manager.expand_path(
    "~/VEGETA_PHASE8_TEST/renamed_test.txt"
)

moved_file = file_manager.expand_path(
    "~/VEGETA_PHASE8_TEST/Destination/renamed_test.txt"
)


# ---------------------------------------------------------
# 1. CREATE TEST FILE
# ---------------------------------------------------------

print("1. Creating test file...")

with open(test_file, "w", encoding="utf-8") as file:
    file.write("VEGETA Phase 8 file operation test.")

print(f"Created -> {test_file}")


# ---------------------------------------------------------
# 2. RENAME
# ---------------------------------------------------------

print()
print("2. Renaming test file...")

result = file_manager.rename(
    test_file,
    "renamed_test.txt"
)

print("Rename result:", result)


# ---------------------------------------------------------
# 3. CREATE DESTINATION FOLDER
# ---------------------------------------------------------

print()
print("3. Creating destination folder...")

result = file_manager.create_folder(
    destination_folder
)

print("Create destination result:", result)


# ---------------------------------------------------------
# 4. MOVE
# ---------------------------------------------------------

print()
print("4. Moving renamed file...")

result = file_manager.move(
    renamed_file,
    destination_folder
)

print("Move result:", result)


# ---------------------------------------------------------
# 5. VERIFY MOVED FILE
# ---------------------------------------------------------

print()
print("5. Checking moved file...")

if moved_file:
    print("Moved file exists:", __import__("os").path.exists(moved_file))


# ---------------------------------------------------------
# 6. OPEN
# ---------------------------------------------------------

print()
print("6. Opening moved file...")

result = file_manager.open_path(
    moved_file
)

print("Open result:", result)


# ---------------------------------------------------------
# 7. DELETE TEST FILE
# ---------------------------------------------------------

print()
print("7. Deleting test file...")

result = file_manager.delete(
    moved_file
)

print("Delete file result:", result)


# ---------------------------------------------------------
# 8. DELETE TEST FOLDER
# ---------------------------------------------------------

print()
print("8. Deleting test folder...")

result = file_manager.delete(
    test_folder
)

print("Delete folder result:", result)


# ---------------------------------------------------------
# COMPLETE
# ---------------------------------------------------------

print()
print("==============================")
print("       TEST COMPLETE")
print("==============================")