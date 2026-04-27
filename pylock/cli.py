import argparse
import getpass
import os
import time
from pylock.commands.gen import handle_password
from pylock.services.clipboard import copy_to_clipboard
from pylock.services.storage import save_secure, load_secure

def main():
    parser = argparse.ArgumentParser(prog="pylock")

    subparsers = parser.add_subparsers(dest="command")

    # gen command
    gen_parser = subparsers.add_parser("gen")
    gen_sub = gen_parser.add_subparsers(dest="type")

    # password subcommand
    pwd_parser = gen_sub.add_parser("password")

    pwd_parser.add_argument("-l", "--length", type=int, default=12)
    pwd_parser.add_argument("-n", "--number", type=int, default=1)

    # Counts (optional)
    pwd_parser.add_argument("-uc", "--uppercase", type=int, nargs="?", const=1)
    pwd_parser.add_argument("-lc", "--lowercase", type=int, nargs="?", const=1)
    pwd_parser.add_argument("-d", "--digits", type=int, nargs="?", const=1)
    pwd_parser.add_argument("-s", "--symbols", type=int, nargs="?", const=1)

    # Exclusions
    pwd_parser.add_argument("--nd", "--no-digits", action="store_true")
    pwd_parser.add_argument("--ns", "--no-symbols", action="store_true")
    pwd_parser.add_argument("--na", "--no-ambiguous", action="store_true")

    # Utilities
    pwd_parser.add_argument("--copy", choices=["first", "last", "all"])
    pwd_parser.add_argument("--save", type=str)

    # decrypt command
    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("file")

    # passphrase subcommand
    # pass_parser = gen_sub.add_parser("passphrase")

    # pass_parser.add_argument("-w", "--words", type=int, default=4)
    # pass_parser.add_argument("--sep", type=str, default="-")
    # pass_parser.add_argument("--caps", action="store_true")
    # pass_parser.add_argument("--copy", action="store_true")
    # pass_parser.add_argument("--save", type=str)

    args = parser.parse_args()

    if args.command == "gen" and args.type == "password":
        try:
            passwords = handle_password(args)
            # print passwords
            for i, p in enumerate(passwords, 1):
                if len(passwords) > 1:
                    print(f"{i}. {p}")
                else:
                    print(p)

            # copy with options
            if args.copy:
                if args.copy == "first":
                    copy_to_clipboard(passwords[0])
                elif args.copy == "last":
                    copy_to_clipboard(passwords[-1])
                elif args.copy == "all":
                    copy_to_clipboard("\n".join(passwords))
                print(f"[✓] Copied to clipboard")
                

            # save all at once with numbering
            if args.save:
                password = getpass.getpass("Enter master password: ")
                
                data = {"passwords": passwords}

                save_secure(args.save, data, password)
                
                print(f"[✓] Saved securely to {args.save}")

                            
        except ValueError as e:
            print(f"[!] {e}")

    if args.command == "decrypt":

        #check if file exists
        if not os.path.exists(args.file):
            print(f"[!] File not found")
            print("[Hint] Check the file name or path")
            return
        
        # attempts to enter correct password
        attempts = 3

        for attempt in range(attempts):
            password = getpass.getpass("Enter master password (input hidden): ")

            try:
                data = load_secure(args.file, password)
                
                print("\nDecrypted Data:")
                for i, p in enumerate(data["passwords"], 1):
                    print(f"{i}. {p}")
                break

            except ValueError as e:
                if str(e) == "corrupted_file":
                    print("[!] File is corrupted or invalid format")
                    print("[Hint] Ensure the file was created by PyLock and not modified")
                    break

                elif str(e) == "invalid_credentials":
                    print(f"[!] Incorrect password ({attempt + 1}/{attempts})")
                    print("[Hint] Make sure you entered the correct master password")
                    time.sleep(1)  # brief pause before next attempt
        else:
            print("[!] Access denied after 3 attempts")

    # if args.command == "gen" and args.type == "passphrase":
    #     phrase = handle_passphrase(args)

    #     if args.copy:
    #         import pyperclip
    #         pyperclip.copy(phrase)

    #     if args.save:
    #         with open(args.save, "a") as f:
    #             f.write(phrase + "\n")

    #     print(phrase)

if __name__ == "__main__":
    main()

