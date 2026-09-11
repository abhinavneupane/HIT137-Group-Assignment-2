def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    with open(input_path, "r") as file:
        text = file.read()

    encrypted_text = ""

    for char in text:
        if 'a' <= char <= 'n':
            shift = shift1 * shift2
            encrypted_text += chr((ord(char) - ord('a') + shift) % 14 + ord('a'))

        elif 'o' <= char <= 'z':
            shift = shift1 + shift2
            encrypted_text += chr((ord(char) - ord('o') - shift) % 12 + ord('o'))

        elif 'A' <= char <= 'M':
            shift = shift1
            encrypted_text += chr((ord(char) - ord('A') - shift) % 13 + ord('A'))

        elif 'N' <= char <= 'Z':
            shift = shift2 * shift2
            encrypted_text += chr((ord(char) - ord('N') + shift) % 13 + ord('N'))

        elif '0' <= char <= '9':
            shift = shift1 - shift2
            encrypted_text += chr((ord(char) - ord('0') + shift) % 10 + ord('0'))

        else:
            encrypted_text += char

    with open(output_path, "w") as file:
        file.write(encrypted_text)


def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    with open(input_path, "r") as file:
        encrypted_text = file.read()

    decrypted_text = ""

    for char in encrypted_text:
        if 'a' <= char <= 'n':
            shift = shift1 * shift2
            decrypted_text += chr((ord(char) - ord('a') - shift) % 14 + ord('a'))

        elif 'o' <= char <= 'z':
            shift = shift1 + shift2
            decrypted_text += chr((ord(char) - ord('o') + shift) % 12 + ord('o'))

        elif 'A' <= char <= 'M':
            shift = shift1
            decrypted_text += chr((ord(char) - ord('A') + shift) % 13 + ord('A'))

        elif 'N' <= char <= 'Z':
            shift = shift2 * shift2
            decrypted_text += chr((ord(char) - ord('N') - shift) % 13 + ord('N'))

        elif '0' <= char <= '9':
            shift = shift1 - shift2
            decrypted_text += chr((ord(char) - ord('0') - shift) % 10 + ord('0'))

        else:
            decrypted_text += char

    with open(output_path, "w") as file:
        file.write(decrypted_text)


def verify_files(original_path: str, decrypted_path: str) -> bool:
    with open(original_path, "r") as file:
        original_text = file.read()

    with open(decrypted_path, "r") as file:
        decrypted_text = file.read()

    if original_text == decrypted_text:
        print("Decryption successful. Files match.")
        return True
    else:
        print("Decryption failed. Files do not match.")
        return False


shift1 = int(input("Enter shift1: "))
shift2 = int(input("Enter shift2: "))

if shift1 < 0 or shift2 < 0:
    print("Error: shift1 and shift2 must be non-negative integers.")

else:
    encrypt_file(
        shift1,
        shift2,
        "raw_text.txt",
        "encrypted_text.txt"
    )

    decrypt_file(
        shift1,
        shift2,
        "encrypted_text.txt",
        "decrypted_text.txt"
    )

    verify_files(
        "raw_text.txt",
        "decrypted_text.txt"
    )