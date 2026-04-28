# 🔐 PyLock

**A modern CLI toolkit for generating, analyzing, and securing credentials.**

PyLock helps you create strong passwords, memorable passphrases, and unique usernames — all from your terminal with a clean and intuitive interface.

---

## ✨ Features

### 🔹 Password Generator

* Custom length (`-l`)
* Character control (digits, symbols, uppercase, lowercase)
* Exclude ambiguous characters (`--na`)
* Generate multiple passwords (`-n`)
* Copy to clipboard / Save securely

---

### 🔹 Passphrase Generator

* Word-based passwords (Diceware-style)
* Custom word count (`-w`)
* Separator control (`--sep`)
* Capitalization support (`--caps`)
* Optional digits
* Copy / Save (encrypted)

---

### 🔹 Username Generator

Generate unique usernames with different styles:

#### 🎯 Vibes

* `clean` → `aanchal.dev`
* `aesthetic` → `hey.aanchal`
* `tech` → `aanchalops`
* `edgy` → `aanchalx`
* `words` → `pixel-orbit` (random word combinations)

#### ⚙️ Options

* Add digits (`-d`)
* Add symbols (`-s`)
* Multiple usernames (`-n`)
* Copy / Save (encrypted)

---

### 🔐 Secure Storage

* Encrypt saved credentials using a master password
* Decrypt anytime with `pylock decrypt <file>`
* Uses modern cryptography (PBKDF2 + Fernet)

---

## 🚀 Installation

```bash
git clone https://github.com/Aanchal-2312/pylock
cd pylock
pip install -e .
```

---

## ⚡ Usage

### Generate Password

```bash
pylock gen password
pylock gen password -l 16 -n 5
```

---

### Generate Passphrase

```bash
pylock gen passphrase -w 4 --caps
```

---

### Generate Username

```bash
pylock gen username --name aanchal --vibe tech
pylock gen username --vibe words -n 5
```

---

### Copy / Save

```bash
pylock gen password --copy
pylock gen password --save creds.json
```

---

### Decrypt File

```bash
pylock decrypt creds.json
```

---

## 🧠 Project Vision

PyLock is being built as a **security-focused CLI toolkit** with:

* Strong defaults
* Clean UX
* Modular architecture
* Real-world usability

Future plans include:

* Password strength analysis
* Policy validation
* Deterministic password generation
* AI-assisted suggestions

---

## 🛠 Tech Stack

* Python
* argparse (CLI)
* cryptography (encryption)
* secrets (secure randomness)

---

## 📌 Status

🚧 Actively under development
Core generation features are complete.

---

