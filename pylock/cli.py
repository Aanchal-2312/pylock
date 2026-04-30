"""
PyLock CLI entry point.
Handles command parsing and routes commands to appropriate handlers.
"""

import argparse
import getpass
import os
import sys
import time

# Local Imports
from pylock.commands.analyze import handle_check
from pylock.commands.gen import handle_password, handle_passphrase, handle_username
from pylock.commands.validate import handle_validate
from pylock.commands.hash import handle_hash
from pylock.commands.verify import handle_verify
from pylock.commands.config import handle_config

from pylock.infra.clipboard import copy_to_clipboard
from pylock.infra.storage import save_secure, load_secure

from pylock.utils.formatter import format_output
from pylock.utils.helper import show_help, show_version


def main():
    """Main CLI Handler"""

    parser = argparse.ArgumentParser(prog="pylock")
    subparsers = parser.add_subparsers(dest="command")
 

    # VERSION COMMAND (aliases)
    v_parser = subparsers.add_parser("version")
    v2_parser = subparsers.add_parser("v")


    # GEN COMMAND SETUP
    gen_parser = subparsers.add_parser("gen")
    gen_sub = gen_parser.add_subparsers(dest="type")

    # PASSWORD SUBCOMMAND
    pwd_parser = gen_sub.add_parser("password")
    pwd_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)
    pwd_parser.add_argument("-l", "--length", type=int, default=12)
    pwd_parser.add_argument("-n", "--number", type=int, default=1)
    # Character controls
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


    # DECRYPT COMMAND
    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("file")


    # PASSPHRASE SUBCOMMAND
    pass_parser = gen_sub.add_parser("passphrase")
    pass_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)
    pass_parser.add_argument("-w", "--words", type=int, default=4)
    pass_parser.add_argument("--sep", type=str, default="-")
    pass_parser.add_argument("--caps", choices=["first", "all"], default=None)
    pass_parser.add_argument("-d","--digits", type=int, default=0) 
    pass_parser.add_argument("-n","--number",type=int,default=1)
    pass_parser.add_argument("--copy", choices=["first","last", "all"], default="last")
    pass_parser.add_argument("--save", type=str)


    # USERNAME SUBCOMMAND
    user_parser = gen_sub.add_parser("username")
    user_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)
    user_parser.add_argument("--vibe", choices=["clean", "aesthetic", "tech", "edgy","random","gamer","words"], default="clean")
    user_parser.add_argument("--name", type=str)
    user_parser.add_argument("-d", "--digits", type=int, default=0)
    user_parser.add_argument("-s", "--symbols", type=int, default=0)
    user_parser.add_argument("--caps", choices=["first", "all"], default="first")
    user_parser.add_argument("-n", "--number", type=int, default=1)
    user_parser.add_argument("--copy", choices=["first", "last", "all"], default="last")
    user_parser.add_argument("--save", type=str)


    # ANALYZE COMMAND
    check_parser = subparsers.add_parser("analyze")
    check_parser.add_argument("password")
    check_parser.add_argument("--strict", action="store_true")
    check_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)


    # VALIDATE COMMAND
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)
    validate_parser.add_argument("password")
    validate_parser.add_argument("--basic", action="store_true")
    validate_parser.add_argument("--min-length", type=int, default=12)
    validate_parser.add_argument("--require-symbols", action="store_true", default=True)
    validate_parser.add_argument("--require-numbers", action="store_true", default=True)
    validate_parser.add_argument("--no-repeats", action="store_true", default=True) 


    # HASH & VERIFY COMMANDS
    hash_parser = subparsers.add_parser("hash")
    hash_parser.add_argument("password")
    hash_parser.add_argument("-f", "--format", choices=["json", "env"], default=None) 
    hash_parser.add_argument("--algo", choices=["bcrypt", "argon2"], default="None")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("password")
    verify_parser.add_argument("hash")
    verify_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)


    # CONFIG COMMAND
    config_parser = subparsers.add_parser("config")
    config_sub = config_parser.add_subparsers(dest="action", required=True)
    show_parser = config_sub.add_parser("show")
    show_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)
    set_parser = config_sub.add_parser("set")
    set_parser.add_argument("key")
    set_parser.add_argument("value")
    set_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)
    reset_parser =config_sub.add_parser("reset")
    reset_parser.add_argument("-f", "--format", choices=["json", "env"], default=None)


    # HANDLE NO ARGUMENTS

    if len(sys.argv) == 1:
        show_help()
        sys.exit()

    args = parser.parse_args()   


    # VERSION
    if args.command == "version" or args.command == "v":
        print(show_version())   


    # PASSWORD GENERATION
    if args.command == "gen" and args.type == "password":
        try:
            passwords = handle_password(args)

            # Format-aware output
            formatted = format_output(passwords, args.format)

            if formatted:
                print(formatted)
            else:
                for i, p in enumerate(passwords, 1):
                    if len(passwords) > 1:
                        print(f"{i}. {p}")
                    else:
                        print(p)

            # Clipboard copy
            if args.copy and not args.format:
                if args.copy == "first":
                    copy_to_clipboard(passwords[0])
                elif args.copy == "last":
                    copy_to_clipboard(passwords[-1])
                elif args.copy == "all":
                    copy_to_clipboard("\n".join(passwords))
                print(f"[✓] Copied to clipboard")
                

            # Secure save
            if args.save and not args.format:
                password = getpass.getpass("Enter master password: ")
                data = {"type": "passwords","data": passwords}
                save_secure(args.save, data, password)
                print(f"[✓] Saved securely to {args.save}")

        except ValueError as e:
            print(f"[!] {e}")



    # DECRYPTION
    if args.command == "decrypt":

        if not os.path.exists(args.file):
            print(f"[!] File not found")
            print("[Hint] Check the file name or path")
            return
        
        attempts = 3   # max password attempts

        for attempt in range(attempts):
            password = getpass.getpass("Enter master password (input hidden): ")

            try:
                data = load_secure(args.file, password)

                if "type" not in data or "data" not in data:
                    print("[!] Invalid file format")
                    print("[Hint] File structure is not recognized")
                    return

                data_type = data["type"]
                items = data["data"]

                print(f"\n🔓 Decrypted {data_type.capitalize()} Data:\n")

                for i, item in enumerate(items, 1):
                    print(f"{i}. {item}")
                break

            except ValueError as e:
                if str(e) == "corrupted_file":
                    print("[!] File is corrupted or in invalid format")
                    print("[Hint] Ensure the file was created by PyLock and not modified")
                    break

                elif str(e) == "invalid_credentials":
                    print(f"[!] Incorrect password ({attempt + 1}/{attempts})")
                    print("[Hint] Make sure you entered the correct master password")
                    time.sleep(1)  # brief pause before next attempt
        else:
            print("[!] Access denied after 3 attempts")



    # PASSPHRASE GENERATION
    if args.command == "gen" and args.type == "passphrase":
        phrases = handle_passphrase(args)

        formatted = format_output(phrases, args.format)

        if formatted:
            print(formatted)
        else:
            for i, p in enumerate(phrases, 1):
                if len(phrases) > 1:
                    print(f"{i}. {p}")
                else:
                    print(p)
       
        if args.copy and not args.format:
            if args.copy == "first":
                copy_to_clipboard(phrases[0])
            elif args.copy == "last":
                copy_to_clipboard(phrases[-1])
            elif args.copy == "all":
                copy_to_clipboard("\n".join(phrases))
            print("[✓] Copied to clipboard")

        if args.save and not args.format:
            password = getpass.getpass("Enter master password: ")
            data = {"type": "passphrases","data": phrases}
            save_secure(args.save, data, password)
            print(f"[✓] Saved securely to {args.save}")



    # USERNAME GENERATION
    if args.command == "gen" and args.type == "username":
        usernames = handle_username(args)

        formatted = format_output(usernames, args.format)

        if formatted:
            print(formatted)
        else:
            for i, u in enumerate(usernames, 1):
                if len(usernames) > 1:
                    print(f"{i}. {u}")
                else:
                    print(u)
        
        if args.copy and not args.format:
            if args.copy == "first":
                copy_to_clipboard(usernames[0])
            elif args.copy == "last":
                copy_to_clipboard(usernames[-1])
            elif args.copy == "all":
                copy_to_clipboard("\n".join(usernames))
            print("[✓] Copied to clipboard")

        if args.save and not args.format:
            password = getpass.getpass("Enter master password: ")
            data = {"type": "usernames","data": usernames}
            save_secure(args.save, data, password)
            print(f"[✓] Saved securely to {args.save}") 



    # ANALYZE COMMAND
    if args.command == "analyze":
        result = handle_check(args)

        formatted = format_output(result, args.format)

        if formatted:
            print(formatted)
        else:
            print("\n🔍 Password Analysis\n")

            print(f"Strength: {result['score']}")
            print(f"Entropy: {result['entropy']} bits")
            print(f"Crack Time: {result['crack_time']}")

            if result["weaknesses"]:
                print("\n⚠ Weaknesses:")
                for w in result["weaknesses"]:
                    print(f"- {w}")

            if result["suggestions"]:
                print("\n💡 Suggestions:")
                for s in result["suggestions"]:
                    print(f"- {s}")  

            if "validation" in result:
                print("\n Policy Check:\n")
                if not result["validation"]:
                    print("✔ Meets strict security requirements")
                else:
                    print("❌ Fails policy rules:\n")
                    for e in result["validation"]:
                        print(f"- {e}")



    # VALIDATE COMMAND
    if args.command == "validate":
        errors = handle_validate(args)

        formatted = format_output(errors, args.format)

        if formatted:
            print(formatted)
        else:
            print("\n🔍 Validation Result\n")

            if not errors:
                print("✔ Password meets all requirements")
            else:
                print("❌ Password failed validation:\n")
                for e in errors:
                    print(f"- {e}")



    # HASH COMMAND
    if args.command == "hash":
        hashed = handle_hash(args)
        formatted = format_output({"hash": hashed}, args.format)

        if formatted:
            print(formatted)
        else:
            print("\n🔑 Hashed Password:\n")
            print(hashed)



    # VERIFY COMMAND
    if args.command == "verify":
        is_valid = handle_verify(args)

        formatted = format_output({"valid": is_valid}, args.format)

        if formatted:
            print(formatted)
        else:
            print("\n🔍 Verification Result:\n")

            if is_valid:
                print("✔ Password matches hash")
            else:
                print("❌ Invalid password")

    
    
    # CONFIG COMMAND
    if args.command == "config":
        result = handle_config(args)
        formatted = format_output(result, args.format)
        if formatted:
            print(formatted)
        else:

            print("\n⚙️ Configuration\n")
            
            if args.action == "set":
                print("✔ Config updated\n")
            elif args.action == "reset":
                print("✔ Config reset to defaults\n")

            if isinstance(result, dict):
                for k, v in result.items():
                    print(f"{k:<18}: {v}")
        



# PROGRAM ENTRY POINT
if __name__ == "__main__":
    main()
