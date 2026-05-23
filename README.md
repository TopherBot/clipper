# Clipper

**Problem**: Quickly copy text to your clipboard from the terminal, with optional AES‑256 encryption for sensitive snippets.

**Features**
- Copy plain text to clipboard.
- Encrypt text before copying (`-e` flag) using a password.
- Decrypt clipboard content (`-d` flag) back to plain text.
- Zero‑dependency on external binaries; uses `pyperclip` and `cryptography` which are installed via the provided `setup.sh`.

**Installation**
```sh
# One‑command setup (requires Python 3.8+ and pip)
curl -sSL https://raw.githubusercontent.com/yourusername/clipper/main/setup.sh | bash
```

**Usage**
```sh
# Copy plain text
clipper "Hello World"

# Copy encrypted text (you will be prompted for a password)
clipper -e "Secret Message"

# Decrypt current clipboard content
clipper -d
```

**License**: MIT
