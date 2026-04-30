"""CLI helper utilities.

Provides help display and version information for PyLock."""

# HELP DISPLAY
def show_help():
    
    """Display CLI usage instructions and examples."""

    help_text = """
🔐 PyLock — Security Toolkit (CLI)

Usage:
  pylock <command> [subcommand] [options]

────────────────────────────────────────

📦 Commands:

  gen         Generate secure values
              ├─ password     Generate passwords
              ├─ passphrase   Generate passphrases
              └─ username     Generate usernames

  decrypt     Decrypt securely saved data
  analyze     Analyze password strength
  validate    Validate password rules
  hash        Hash a password (bcrypt / argon2)
  verify      Verify password against hash
  config      Manage configuration settings
  version     Show current version

────────────────────────────────────────

⚡ Examples:

  pylock gen password -n 3
  pylock gen password -l 16 --symbols --copy first

  pylock gen passphrase -w 4 --caps first
  pylock gen username --vibe tech --name aanchal

  pylock analyze mypassword --strict
  pylock validate mypassword

  pylock hash mypassword --algo argon2
  pylock verify mypassword <hash>

  pylock decrypt secrets.json

  pylock config show
  pylock config set min_length 16

────────────────────────────────────────

💡 Tips:

  • Use -f json or -f env for machine-readable output
  • Use --copy to copy results directly to clipboard
  • Use --save to securely store generated data
  • Avoid predictable passwords — use passphrases for better security

────────────────────────────────────────
"""
    print(help_text.strip())



# VERSION INFO
def show_version():
  """Return current PyLock version."""
  return "PyLock v1.0.0"