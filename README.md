# 🔐 PyLock

A powerful CLI-based security toolkit for generating, analyzing, validating, and managing credentials.

Built with a focus on **security, usability, and clean developer experience**.

---

## 🚀 Features

### 🔐 Generation

* Secure password generator with full control (length, symbols, digits, ambiguity)
* Passphrase generator using wordlists (human-readable & strong)
* Username generator with multiple vibes:

  * clean, aesthetic, tech, edgy, gamer, words

---

### 🧠 Security Analysis

* Password strength scoring (Very Weak → Very Strong)
* Entropy calculation
* Crack time estimation
* Detection of:

  * common passwords
  * patterns (e.g., `password123`)
  * repeated characters
* Smart suggestions for improvement

---

### 🔍 Validation

* Policy-based validation:

  * minimum length
  * required symbols
  * required numbers
  * no repeated characters
* Configurable defaults

---

### 🔑 Cryptography

* Secure hashing:

  * bcrypt
  * argon2
* Password verification

---

### ⚙️ Utilities

* Copy output to clipboard
* Save encrypted data to file
* Secure decryption
* Output formats:

  * JSON
  * `.env`

---

### ⚙️ Configuration

* View current config
* Set global defaults for validation and hashing
* Reset to defaults

---

### 🧪 Tested & Reliable

* Built with modular architecture
* Core logic fully tested using `pytest`

---

## 📦 Installation

```bash
git clone https://github.com/Aanchal-2312/pylock.git
cd pylock
pip install -r requirements.txt
pip install -e .
```

---

## ⚡ Usage

### 🔐 Generate Passwords

```bash
pylock gen password -n 3
```

### 🔐 Generate Passphrase

```bash
pylock gen passphrase -w 4 --caps first
```

### 👤 Generate Username

```bash
pylock gen username --vibe tech --name aanchal
```

---

### 🧠 Analyze Password

```bash
pylock analyze mypassword --strict
```

---

### 🔍 Validate Password

```bash
pylock validate mypassword
```

---

### 🔑 Hash Password

```bash
pylock hash mypassword --algo argon2
```

---

### 🔑 Verify Password

```bash
pylock verify mypassword "<hash>"
```

---

### 💾 Save & Decrypt

```bash
pylock gen password --save creds.json
pylock decrypt creds.json
```

---

### 📤 Output Formats

```bash
pylock gen password -n 2 -f json
pylock validate mypass -f env
```

---

### ⚙️ Config

```bash
pylock config show
pylock config set default_algo argon2
```

---

## 🧠 Design

* Modular architecture:

  * `commands/` → CLI handling
  * `core/` → logic
  * `infra/` → storage, clipboard, wordlists
  * `utils/` → formatting & helpers
* Secure defaults
* Clean CLI UX

---

## 📌 Version

```bash
pylock version
```

---

## 💛 Author

Built with focus and intention by **Aanchal**

---


