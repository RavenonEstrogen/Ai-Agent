from functions.get_files_info import get_files_info

test_1 = get_files_info("calculator", ".")
print("Result for current directory:")
print(test_1)

test_2 = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
print(test_2)

test_3 = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(test_3)

test_4 = get_files_info("calculator", "../")
print("Result for '../' directory:")
print(test_4)