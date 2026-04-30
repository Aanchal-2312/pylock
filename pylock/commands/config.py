from pylock.core.config import load_config, set_config, reset_config


def handle_config(args) :
    """Handle the configuration commands (show, set, reset)."""

    if args.action == "show":
        return load_config()

    elif args.action == "set":
        return set_config(args.key, args.value)

    elif args.action == "reset":
        return reset_config()