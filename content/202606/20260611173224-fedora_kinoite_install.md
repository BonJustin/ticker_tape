---
title: Linux Initial Installation
keywords: [computer reference, linux, fedora, kinoite]
abstract: This is a rough outline of my initial Fedora Kinoite installtion. I have tried to modify it as I alter bits and pieces of the system, though this is proving difficult to keep up with.
date: 2026-06-11 17:32:24
---

## Fedora on NVMe M.2

I recently ordered a new Framework laptop that will be delivered in 3 months. My current desktop runs Windows 11 Pro. My desktop has two internal NVME M.2 drives and a third SATA SSD. The default boot drive is a 4 TB drive. The second NVME M.2 drive is 2 TB and was not in use. The third is a 2 TB SATA SSD used as a data only archive.

I want to run the new Framework laptop with Fedora (Linux). I have downloaded and installed Fedora Workstation on the secondary NVME M.2 (2 TB). I want to set up this drive to be fully prepared for installation on the Framework laptop when it arrives.

My philosophical purpose is to "digitally decouple" from SaaS where possible but maintain professional grade compute power. I will maintain my Windows 11 Pro environment as migrating to Linux will take significant time and effort.

## Fedora version

I have decided to try Kinoite for immutability and security. I will need to review the notes in this plan and alter as needed.

## Laptop Purposes

* Python development with use of `uv`
  * Zed IDE initially. I will consider VS Code later if I am dissatisfied.
  * Beyond the Python standard library, I frequently use openai, matplotlib, numpy, pypandoc, seaborn, and pandas.
* Photography image archive and editing. I currently use Adobe Photoshop and Bridge, but will be migrating to alternatives.
  * Currently investigating digiKAM, darktable, rawtherapee, and gimp.
* Local LLM inference and programming via Python and use via chat with LLaMa.cpp and Hugging Face quantized GGUF or better alternative if one exists. I can prepare the software and download the models prior to receiving the new laptop, but I can't actually run them as my GPU/CPU/VRAM/RAM profile will be entirely different on the new machine than on my desktop.
* Moderate gaming via Steam depending on games available in my Steam library.
* Extensive CLI utility support and scripting. Rclone, 7zip or alternative, Picocrypt, StatiCrypt, Pandoc, Something akin to HWInfo, Veracrypt (or alternative), possibly LaTeX, Typst, etc... pretty sure this implies Node.js among others.)
* Tor Browser and Onion capacity in addition to Firefox.
* I carry Tails OS on a flash drive for secure amnesic communications standards, this should work on the new laptop.
* I want to be very careful about anonymity and security, isolating effects on the OS, and exposure to threat vectors, without disabling my computer function.
* Kiwix and offline English Wikipedia, extensive OpenStax PDF textbook library.

## Implementation Plan

### 1

* Install Fedora (Kinoite) with encryption enabled. I used Fedora Media Writer on Windows to make a bootable USB (16 GB) that installs Kinoite. Kinoite is an atomic/immutable Fedora that uses the KDE Plasma GUI.

### 2

* Update the immutable system image.

```bash
rpm-ostree upgrade
```
*(Note: If updates are applied, you will need to reboot to slide into the new system deployment).*

### 3

* Ensure Flathub is enabled and install Flatseal for managing sandbox permissions.

```bash
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.github.tchx84.Flatseal -y
```

### 4

* Install `uv` (installs cleanly into your writable user space under `~/.local/bin`).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv --version
```

### 5

* Install Python for development (completely isolated from the host).

```bash
uv python install 3.14.5
```

### 6

*I haven't needed this yet.*

* **Toolbx / Distrobox Considerations:** On Kinoite, you cannot easily install system-level library headers (`-devel` packages) on the host system. Therefore, if a Python package requires compiling C-extensions and throws errors about missing system headers, you **must** use Toolbx or Distrobox.
  * Create a development container: `toolbox create`
  * Enter it: `toolbox enter`
  * Install your development libraries inside the container via `dnf`.

### 7

* Install Zed (installs to user space via `~/.local`).

```bash
curl -f https://zed.dev/install.sh | sh
```

### 8

* Install ruff via `uv` as a globally available Zed linter.

```bash
uv tool install ruff
```

### 9

* Install Markdownlint (an extension for Zed).
  1. Command palette `Ctrl + Shift + P`.
  2. Search for `zed: extensions`.
  3. Find **Markdownlint** and click **Install**.

### 10

* Install Node.js via **`fnm`** (Fast Node Manager) instead of `dnf`. This keeps Node.js and all global NPM packages completely inside your user space, removing the need for `sudo` or global prefix workarounds.

```bash
# Install fnm
curl -fsSL https://fnm.vercel.app/install | bash
source ~/.bashrc

# Install and use the latest Long-Term Support (LTS) version of Node.js
fnm install --lts
fnm use lts-latest
node -v
npm -v
```

### 11

* Install Typst CLI. Download the precompiled static binary directly to your user space `~/.local/bin` to keep the host system clean.

```bash
# Download, extract, and copy the static binary
# Ensure your user-space bin directory exists
mkdir -p ~/.local/bin

# Download the correct .tar.xz archive
wget https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz

# Extract using the standard tar extraction flag (automatically handles .xz)
tar -xf typst-x86_64-unknown-linux-musl.tar.xz

# Copy the binary to your local bin path
cp typst-x86_64-unknown-linux-musl/typst ~/.local/bin/

# Clean up downloaded files
rm -rf typst-x86_64-unknown-linux-musl*
```

### 12

* Install the Typst extension for Zed.

### 13

* Zed `settings.json` configuration

```json
// Zed settings
//
// For information on how to configure Zed, see the Zed
// documentation: https://zed.dev/docs/configuring-zed
//
// To see all of Zed's default settings without changing your
// custom settings, run `zed: open default settings` from the
// command palette (cmd-shift-p / ctrl-shift-p)
{
  "project_panel": {
    "dock": "left",
  },
  "minimap": {
    "show": "always",
  },
  "soft_wrap": "editor_width",
  "ui_font_size": 16,
  "buffer_font_size": 15,
  "theme": "One Dark",
  "restore_on_startup": "last_session",
  "session": {
    "restore_unsaved_buffers": true,
  },
  "lsp": {
    // Markdownlint settings to remove warnings regarding
    //  line-length, raw HTML tags, and supress warnings about
    //  missing top level headers.
    "markdownlint": {
      "settings": {
        "MD013": false,
        "MD033": false,
        "MD041": false,
      },
    },
    "tinymist": {
      "initialization_options": {
        "preview": {
          "background": {
            "enabled": true,
          },
        },
      },
      "settings": {
        "exportPdf": "onSave",
        "outputPath": "$root/$name",
        "formatterMode": "typstyle",
        "lint": {
          "enabled": true,
          "when": "onSave",
        },
      },
    },
  },
  // Disable telemetry.
  "telemetry": {
    "diagnostics": false,
    "metrics": false,
  },
  "languages": {
    // Python linting settings for ruff. To turn off the auto-corrections,
    // remove code_action and language_server blocks and turn format_on_save to off.
    "Python": {
      "language_servers": ["basedpyright", "ruff"],
      "format_on_save": "on",
      "formatter": [
        {
          "code_action": "source.organizeImports.ruff",
        },
        {
          "code_action": "source.fixAll.ruff",
        },
        {
          "language_server": {
            "name": "ruff",
          },
        },
      ],
    },
    "Markdown": {
      "tab_size": 4,
      "hard_tabs": false,
    },
    "Typst": {
      "language_servers": ["tinymist"],
      "formatter": {
        "language_server": {
          "name": "tinymist",
        },
      },
      "format_on_save": "on",
    },
  },
}
```

### 14

* Install Rclone in user space as a standalone binary (avoids layering software on the host).

```bash
curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip
cd rclone-v*-linux-amd64
cp rclone ~/.local/bin/
cd ..
rm -rf rclone-current-linux-amd64.zip rclone-v*-linux-amd64
```

### 15

Set up Rclone for WebDAV access.
* `rclone config`
* `n` for new remote
* Name the remote
* `webdav` storage type
* Enter WebDAV URL, username, and password

### 16

* Install KeePassXC using Flatpak.

*Note: KeePassXC is a password manager application using KeePass. I can set it up to sync with a WebDAV on my VPS. There is an iPhone app called KeePassium that also uses KeePass, and it syncs with the same WebDAV folder on my server. On desktop, I have a bash script that must be run prior to using KeePassXC. It syncs a local copy of the KeePass database with the WebDAV server. KeePassium also keeps an offline copy. KeePassXC runs on Windows as well, but I have not set it up to sync with the WebDAV server, so I am not using it.*

```bash
flatpak install flathub org.keepassxc.KeePassXC
```

### 17

* Create a directory in your writable `/home` partition for WebDAV use.

```bash
mkdir -p ~/webdav/keepass
```

### 18

* Test mounting the WebDAV folder:

```bash
rclone mount jmbsquared_keepass: ~/webdav/keepass \
--vfs-cache-mode full \
--exclude ".*"
```

### 19

* Create the synchronization script `~/.local/bin/keepass_sync.sh` (unchanged, as `/home` paths remain writable).

```bash
#!/bin/bash

# Configuration
LOCAL_DIR="$HOME/webdav/keepass"
REMOTE_NAME="jmbsquared_keepass:"
LOG_FILE="$HOME/.cache/rclone/keepass_sync_log.txt"

# Safety Check
if [ ! -f "$LOCAL_DIR/RCLONE_TEST" ]; then
    echo "ERROR: Safety marker RCLONE_TEST not found in $LOCAL_DIR"
    read -p "Press enter to exit..."
    exit 1
fi

echo "Starting KeePass Sync..."

# STEP 1: Pull from Server to Local
# --update: Only copy if the source (remote) is newer than the destination (local)
# --exclude: Strictly ignore the .ht files to avoid 403 errors
echo "Checking for server updates..."
rclone copy "$REMOTE_NAME" "$LOCAL_DIR" \
    --update \
    --modify-window 10s \
    --exclude ".ht*" \
    --verbose --log-file=$LOG_FILE

# STEP 2: Push from Local to Server
# --update: Only copy if the local file is newer than the server file
echo "Uploading local changes..."
rclone copy "$LOCAL_DIR" "$REMOTE_NAME" \
    --update \
    --modify-window 10s \
    --exclude ".ht*" \
    --verbose --log-file=$LOG_FILE

echo ""
read -n 1 -s -r -p "Sync Complete. Press any key to close this window..."
```

* Make it executable:

```bash
chmod +x ~/.local/bin/keepass_sync.sh
```

* Create the desktop shortcut launcher in `~/.local/share/applications/keepass_sync.desktop`:

```
[Desktop Entry]
Type=Application
Version=1.0
Name=KeePass_Sync
Comment=Sync database with WebDAV and Launch KeePassXC
Exec=/home/bonju/.local/bin/keepass_sync.sh
Icon=utilities-terminal
Terminal=true
StartupNotify=false
Categories=Utility;Security;
```

### 20

* Install Pandoc as a standalone user-space binary to avoid pulling in hundreds of megabytes of Haskell system dependencies on your host.

```bash
# Download, extract, and copy the binary to ~/.local/bin
wget https://github.com/jgm/pandoc/releases/download/3.1.11.1/pandoc-3.1.11.1-linux-amd64.tar.gz
tar -xzf pandoc-3.1.11.1-linux-amd64.tar.gz
cp pandoc-3.1.11.1/bin/pandoc ~/.local/bin/
rm -rf pandoc-3.1.11.1*
```

### 21

* Install KaTeX in your user space. Because we are using `fnm` for Node.js, this will sit cleanly within your user profile directory.

```bash
npm install katex --prefix ~/.local/share
```

### 22

* Install Libertinus and Stix Two fonts at the user level to `~/.local/share/fonts/` (system-wide font directories are read-only).

### 23

* Install StatiCrypt using npm (managed automatically by `fnm`'s user-space environment).

```bash
npm install -g staticrypt
```

### 24

* Install Picocrypt via Flatpak.

```bash
flatpak install flathub io.github.picocrypt_ng.Picocrypt-NG
```

*(Use Flatseal to adjust directory access permissions as needed).*

### 25

* Install Kiwix via Flatpak.

```bash
flatpak install flathub org.kiwix.desktop
```

*(Use Flatseal to expose your `.zim` database storage directory to the Kiwix sandbox).*

### 26

* Install Steam via Flatpak.

```bash
flatpak install flathub com.valvesoftware.Steam
```

* **Hardware Controller Integration:** Because Steam is sandboxed in a Flatpak, you must layer the controller hardware integration package on your host system using `rpm-ostree`. This requires a reboot to take effect.

***Note:** I have not installed devices yet…*

```bash
rpm-ostree install steam-devices
```

* Install ProtonUp-Qt via Flatpak to manage game compatibility layers:

```bash
flatpak install flathub net.davidotek.pupgui2
```

### 27

Install Distrobox (a more fully-featured container app than Toolbx) for use when needed.

```bash
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --prefix ~/.local
```

### 28

Install digiKam via flatpak. Many configuration options must be evaluated and refined to prevent xmp collisions with darktable.

### 29

Install GIMP and the G'MIC and Resynthesizer plugins.

```bash
flatpak install flathub org.gimp.GIMP -y
flatpak install flathub org.gimp.GIMP.Plugin.GMic -y
flatpak install flathub org.gimp.GIMP.Plugin.Resynthesizer -y
```

Launch GIMP to initialize, then close and install PhotoGIMP

```bash
wget https://github.com/Diolinux/PhotoGIMP/archive/refs/heads/master.zip -O photogimp.zip
```

Extract and move the /PhotoGIMP-master directory to ~/.var/app/org.gimp.GIMP.

### 30

Install darktable via Flatpak

I used the KDE native application downloader for this one. Darktable also required extensive check of settings to ensure that XMP is never compressed, is created on import, and to look for xmp files on startup. There were more settings, read through and evaluate each very carefully.

### 31

Install Proton VPN, Proton Mail Bridge and Thunderbird and configure. (Flatpak).

### 32

Install Pagefind standalone binary in ~/.local/bin

```bash
mkdir -p ~/.local/bin
curl -LsSf https://pagefind.app/install.sh | sh
```

Test with `pagefind --version`.

### 33

Installed Firefox as a Flatpak. This is better than using the default, as the default can lose settings if a GRUB rollback is necessary. It can be installed via the Discover app. Verify it is the one used by default via usual launch method in use.

Installed basic extensions: **uBlock Origin** and **Firefox Multi-Account Containers**.

* **uBlock Origin** is an ad/content blocker and helps prevent trackers and popups.
* **Firefox Multi-Account Containers** separates tabs into isolated containers. Websites can be kept in specific containers, and data/cookies/etc. from one container cannot see the others. You can log into separate accounts in different containers for the same service.
