from mover import move_duplicates
from verifier import verify_duplicates

if __name__ == "__main__":
    print("Duplicate Manager Tool")
    print("1. Move Duplicates Only")
    print("2. Verify Duplicates Only")
    print("3. Move and then Verify")
    choice = input("Choose an option (1/2/3): ").strip()

    source = input("Enter source folder path: ").strip()
    destination = input("Enter destination folder path: ").strip()

    if choice == "1":
        move_duplicates(source, destination)
    elif choice == "2":
        verify_duplicates(source, destination)
    elif choice == "3":
        move_duplicates(source, destination)
        verify_duplicates(source, destination)
    else:
        print("Invalid choice.")
