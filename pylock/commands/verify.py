from pylock.core.hasher import verify_password


def handle_verify(args):
    """Handle password verification against hash."""
    return verify_password(args.password, args.hash)