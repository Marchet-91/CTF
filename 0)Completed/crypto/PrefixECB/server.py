from chall import encryption_oracle


def start_server():
    while True:
        user_input = input("Input a string to encrypt (input 'q' to quit): ")
        if user_input == 'q':
            break

        output = encryption_oracle(user_input.encode())
        print("Here is your encrypted string, have a nice day :)")
        print(output)


if __name__ == '__main__':
    start_server()
