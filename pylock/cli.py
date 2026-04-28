import argparse
import getpass
import os
import time
from pylock.commands.gen import handle_password, handle_passphrase, handle_username
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
    pass_parser = gen_sub.add_parser("passphrase")

    pass_parser.add_argument("-w", "--words", type=int, default=4)
    pass_parser.add_argument("--sep", type=str, default="-")
    pass_parser.add_argument("--caps", choices=["first", "all"], default=None)

    pass_parser.add_argument("-d","--digits", type=int, default=0) 
    pass_parser.add_argument("-n","--number",type=int,default=1)

    pass_parser.add_argument("--copy", choices=["first","last", "all"], default="last")
    pass_parser.add_argument("--save", type=str)

    # username subcommand
    user_parser = gen_sub.add_parser("username")

    user_parser.add_argument("--vibe", choices=["clean", "aesthetic", "tech", "edgy","random","gamer","words"], default="clean")
    user_parser.add_argument("--name", type=str)

    user_parser.add_argument("-d", "--digits", type=int, default=0)
    user_parser.add_argument("-s", "--symbols", type=int, default=0)
    user_parser.add_argument("--caps", choices=["first", "all"], default="first")

    user_parser.add_argument("-n", "--number", type=int, default=1)

    user_parser.add_argument("--copy", choices=["first", "last", "all"], default="last")
    user_parser.add_argument("--save", type=str)  

    args = parser.parse_args()

    # Handle Password Generation
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
                
                data = {
                    "type": "passwords",
                    "data": passwords
                }

                save_secure(args.save, data, password)
                
                print(f"[✓] Saved securely to {args.save}")

                            
        except ValueError as e:
            print(f"[!] {e}")

    # Handle Decryption
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

                # ✅ validation
                if "type" not in data or "data" not in data:
                    print("[!] Invalid file format")
                    print("[Hint] File structure is not recognized")
                    return

                data_type = data["type"]
                items = data["data"]

                # 🔥 UX upgrade
                print(f"\n🔓 Decrypted {data_type.capitalize()} Data:\n")

                for i, item in enumerate(items, 1):
                    print(f"{i}. {item}")
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

    # Handle Passphrase Generation
    if args.command == "gen" and args.type == "passphrase":
        phrases = handle_passphrase(args)

        # print
        for i, p in enumerate(phrases, 1):
            if len(phrases) > 1:
                print(f"{i}. {p}")
            else:
                print(p)

        # copy
        if args.copy:
            if args.copy == "first":
                copy_to_clipboard(phrases[0])
            elif args.copy == "last":
                copy_to_clipboard(phrases[-1])
            elif args.copy == "all":
                copy_to_clipboard("\n".join(phrases))
            print("[✓] Copied to clipboard")

        # save (secure)
        if args.save:
            password = getpass.getpass("Enter master password: ")
            data = {
                "type": "passphrases",
                "data": phrases
            }
            save_secure(args.save, data, password)
            print(f"[✓] Saved securely to {args.save}")


    # Handle Username Generation
    if args.command == "gen" and args.type == "username":
        usernames = handle_username(args)

        # print
        for i, u in enumerate(usernames, 1):
            if len(usernames) > 1:
                print(f"{i}. {u}")
            else:
                print(u)

        # copy
        if args.copy:
            if args.copy == "first":
                copy_to_clipboard(usernames[0])
            elif args.copy == "last":
                copy_to_clipboard(usernames[-1])
            elif args.copy == "all":
                copy_to_clipboard("\n".join(usernames))
            print("[✓] Copied to clipboard")

        # save
        if args.save:
            password = getpass.getpass("Enter master password: ")
            data = {
                "type": "username",
                "data": usernames
            }
            save_secure(args.save, data, password)
            print(f"[✓] Saved securely to {args.save}") 

# Entry point
if __name__ == "__main__":
    main()

