---
title: "Notes On Transition from VPS to Github"
keywords: [computer reference, log, github, github pages, github actions, jmbsquared.com]
abstract: I am working on transitioning my current website (jmbsquared.com) to Github, and using a CI/CD pipeline to generate the SSG from Markdown.
---

# 1. Project Identity & Philosophy
*   **Nature:** A custom Static Site Generator (SSG) pipeline transforming a Zettelkasten-style Markdown repository into a secure, searchable, static HTML site.
*   **Core Philosophy:** **Software Agnosticism and Archival Purity.** The system prioritizes plain-text Markdown as the source of truth, avoiding proprietary "Vault" structures (e.g., Obsidian) to ensure long-term data retrieval without dependency on specific software.
*   **Organization:** Content is stored using temporal Unique Identifiers (UIDs: `YYYYMMDDHHMMSS`) and chronological bucketing (`YYYYMM` folders).

# 2. Technical Stack (The Toolchain)
*   **Orchestration:** Python (`build_site.py`) managing a linear build pipeline.
*   **Conversion:** Pandoc $\rightarrow$ HTML (via Lua filters for link resolution) and Pandoc $\rightarrow$ Typst $\rightarrow$ PDF.
*   **Search:** Pagefind (chunked, client-side indexing of titles and keywords).
*   **Security:** StatiCrypt (client-side AES encryption) for tiered access: Public, Guest, and Personal.
*   **Frontend:** Pico.css, KaTeX (mathematics), and custom HTML templates.
*   **Local Discovery:** Transitioning to a high-performance CLI stack: `fd`, `fzf`, and `ripgrep`.

# 3. Current Objectives
*   **Primary Goal:** Migrate from a manual VPS deployment to a zero-cost, automated CI/CD pipeline using Github.
*   **Infrastructure Shift:** Local Build $\rightarrow$ **GitHub Actions** (Ephemeral VM for computation) $\rightarrow$ **GitHub Pages** (Static Hosting).
*   **UX Goal:** Create a "Managed Service" model for non-technical contributors, allowing them to write in Markdown (potentially via web-UI) while the pipeline handles the technical build/deploy sequence.
*   **Security Shift:** Move raw passwords from `config.yaml` to **GitHub Actions Secrets** to prevent credential leakage in Git history.

# 4. Current Status

* Created a new private repository: `ticker_tape` as a project root on github.

* Created a new local development directory and copied relevant files to be edited (locally).

* Created a local root project directory and copied relevant files.

***

**~/dev/ticker_tape/**

```
.
├── build
│   ├── assets
│   │   ├── css
│   │   │   ├── custom_002.css
│   │   │   └── pico.css
│   │   ├── fonts
│   │   │   ├── jetbrainsmono-variablefont_wght-webfont.woff2
│   │   │   ├── libertinusserif-bolditalic-webfont.woff2
│   │   │   ├── libertinusserif-bold-webfont.woff2
│   │   │   ├── libertinusserif-italic-webfont.woff2
│   │   │   └── libertinusserif-regular-webfont.woff2
│   │   ├── js
│   │   │   └── pico_pagefind.js
│   │   └── katex
│   │       ├── contrib
│   │       │   ├── auto-render.js
│   │       │   ├── auto-render.min.js
│   │       │   ├── auto-render.mjs
│   │       │   ├── copy-tex.js
│   │       │   ├── copy-tex.min.js
│   │       │   ├── copy-tex.mjs
│   │       │   ├── mathtex-script-type.js
│   │       │   ├── mathtex-script-type.min.js
│   │       │   ├── mathtex-script-type.mjs
│   │       │   ├── mhchem.js
│   │       │   ├── mhchem.min.js
│   │       │   ├── mhchem.mjs
│   │       │   ├── render-a11y-string.js
│   │       │   ├── render-a11y-string.min.js
│   │       │   └── render-a11y-string.mjs
│   │       ├── fonts
│   │       │   ├── KaTeX_AMS-Regular.ttf
│   │       │   ├── KaTeX_AMS-Regular.woff
│   │       │   ├── KaTeX_AMS-Regular.woff2
│   │       │   ├── KaTeX_Caligraphic-Bold.ttf
│   │       │   ├── KaTeX_Caligraphic-Bold.woff
│   │       │   ├── KaTeX_Caligraphic-Bold.woff2
│   │       │   ├── KaTeX_Caligraphic-Regular.ttf
│   │       │   ├── KaTeX_Caligraphic-Regular.woff
│   │       │   ├── KaTeX_Caligraphic-Regular.woff2
│   │       │   ├── KaTeX_Fraktur-Bold.ttf
│   │       │   ├── KaTeX_Fraktur-Bold.woff
│   │       │   ├── KaTeX_Fraktur-Bold.woff2
│   │       │   ├── KaTeX_Fraktur-Regular.ttf
│   │       │   ├── KaTeX_Fraktur-Regular.woff
│   │       │   ├── KaTeX_Fraktur-Regular.woff2
│   │       │   ├── KaTeX_Main-BoldItalic.ttf
│   │       │   ├── KaTeX_Main-BoldItalic.woff
│   │       │   ├── KaTeX_Main-BoldItalic.woff2
│   │       │   ├── KaTeX_Main-Bold.ttf
│   │       │   ├── KaTeX_Main-Bold.woff
│   │       │   ├── KaTeX_Main-Bold.woff2
│   │       │   ├── KaTeX_Main-Italic.ttf
│   │       │   ├── KaTeX_Main-Italic.woff
│   │       │   ├── KaTeX_Main-Italic.woff2
│   │       │   ├── KaTeX_Main-Regular.ttf
│   │       │   ├── KaTeX_Main-Regular.woff
│   │       │   ├── KaTeX_Main-Regular.woff2
│   │       │   ├── KaTeX_Math-BoldItalic.ttf
│   │       │   ├── KaTeX_Math-BoldItalic.woff
│   │       │   ├── KaTeX_Math-BoldItalic.woff2
│   │       │   ├── KaTeX_Math-Italic.ttf
│   │       │   ├── KaTeX_Math-Italic.woff
│   │       │   ├── KaTeX_Math-Italic.woff2
│   │       │   ├── KaTeX_SansSerif-Bold.ttf
│   │       │   ├── KaTeX_SansSerif-Bold.woff
│   │       │   ├── KaTeX_SansSerif-Bold.woff2
│   │       │   ├── KaTeX_SansSerif-Italic.ttf
│   │       │   ├── KaTeX_SansSerif-Italic.woff
│   │       │   ├── KaTeX_SansSerif-Italic.woff2
│   │       │   ├── KaTeX_SansSerif-Regular.ttf
│   │       │   ├── KaTeX_SansSerif-Regular.woff
│   │       │   ├── KaTeX_SansSerif-Regular.woff2
│   │       │   ├── KaTeX_Script-Regular.ttf
│   │       │   ├── KaTeX_Script-Regular.woff
│   │       │   ├── KaTeX_Script-Regular.woff2
│   │       │   ├── KaTeX_Size1-Regular.ttf
│   │       │   ├── KaTeX_Size1-Regular.woff
│   │       │   ├── KaTeX_Size1-Regular.woff2
│   │       │   ├── KaTeX_Size2-Regular.ttf
│   │       │   ├── KaTeX_Size2-Regular.woff
│   │       │   ├── KaTeX_Size2-Regular.woff2
│   │       │   ├── KaTeX_Size3-Regular.ttf
│   │       │   ├── KaTeX_Size3-Regular.woff
│   │       │   ├── KaTeX_Size3-Regular.woff2
│   │       │   ├── KaTeX_Size4-Regular.ttf
│   │       │   ├── KaTeX_Size4-Regular.woff
│   │       │   ├── KaTeX_Size4-Regular.woff2
│   │       │   ├── KaTeX_Typewriter-Regular.ttf
│   │       │   ├── KaTeX_Typewriter-Regular.woff
│   │       │   └── KaTeX_Typewriter-Regular.woff2
│   │       ├── katex.css
│   │       ├── katex.js
│   │       ├── katex.min.css
│   │       ├── katex.min.js
│   │       ├── katex.mjs
│   │       ├── katex-swap.css
│   │       ├── katex-swap.min.css
│   │       └── README.md
│   ├── build_site.py
│   ├── config.yaml
│   ├── pandoc_md_to_static_html.yaml
│   ├── root
│   │   ├── 401.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── 503.html
│   │   ├── apple-touch-icon.png
│   │   ├── favicon-96x96.png
│   │   ├── favicon.ico
│   │   ├── favicon.svg
│   │   ├── index.html
│   │   ├── robots.txt
│   │   ├── site.webmanifest
│   │   ├── web-app-manifest-192x192.png
│   │   └── web-app-manifest-512x512.png
│   ├── templates
│   │   └── md_to_static_html.html
│   └── translate_links.lua
├── content
└── pyproject.toml
```

***

**build_site.py**

```python
import argparse
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

# ===========================================================================
# 1. CONFIGURATION LOADING & GLOBAL INITIALIZATION
# ===========================================================================


def load_config(filename: str = "config.yaml") -> dict:
    """Parses the YAML configuration file securely."""
    path = Path(__file__).parent.resolve() / filename
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


try:
    PROJECT_ROOT = Path(__file__).parent.resolve().parent

    cfg = load_config()
    paths = cfg.get("paths", {})

    SRC = PROJECT_ROOT / paths["src"]
    DST = PROJECT_ROOT / paths["dst"]
    app_dir = PROJECT_ROOT / paths["app"]

    DEFAULTS_YAML = app_dir / "pandoc_md_to_static_html.yaml"
    TEMPLATE_HTML = app_dir / "templates" / "md_to_static_html.html"
    LUA_FILTER = app_dir / "translate_links.lua"
    STATICRYPT_CONFIG = PROJECT_ROOT / ".staticrypt.json"

    # Extract navigation menu and safely format it as a list
    raw_nav = cfg.get("navigation_menu", [])
    if isinstance(raw_nav, list):
        NAVIGATION_MENU = raw_nav
    elif raw_nav:
        NAVIGATION_MENU = [raw_nav]
    else:
        NAVIGATION_MENU = ["index"]

except (FileNotFoundError, KeyError, yaml.YAMLError) as error:
    print(
        f"CRITICAL CONFIGURATION ERROR: Missing value or file: {error}", file=sys.stderr
    )
    sys.exit(1)

# ===========================================================================
# 2. FUNCTION DEFINITIONS
# ===========================================================================


def parse_args():
    p = argparse.ArgumentParser(description="Build HTML site from markdown folder.")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without doing it.",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Show each pandoc command before running it.",
    )
    return p.parse_args()


def extract_custom_template_stream(
    md_path: Path, app_dir: Path, default_template: Path
) -> Path:
    """
    Parses the YAML frontmatter of a markdown file strictly within the start
    and end delimiters ('---'). Fast-paths the template check and resolves
    the template path against the 'app' directory from config.yaml.
    """
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            first_line = f.readline()
            if not first_line:
                return default_template

            # Handle UTF-8 Byte Order Mark (BOM) if present
            if first_line.startswith("\ufeff"):
                first_line = first_line[1:]

            # Standard YAML frontmatter must start on the absolute first line
            if first_line.strip() != "---":
                return default_template

            yaml_lines = []
            closed_properly = False
            # Limit scan to 150 lines to prevent reading entire massive files
            for _ in range(150):
                line = f.readline()
                if not line:
                    break
                if line.strip() == "---":
                    closed_properly = True
                    break
                yaml_lines.append(line)

        # Only parse if we isolated a completely closed, valid frontmatter block
        if closed_properly and yaml_lines:
            yaml_block = "".join(yaml_lines)

            # Fast-path lookup: check if our custom tag exists in the isolated block
            if "html_template" not in yaml_block:
                return default_template

            # Safely load the isolated YAML snippet
            metadata = yaml.safe_load(yaml_block)
            if isinstance(metadata, dict):
                custom_tpl = metadata.get("html_template")
                if custom_tpl:
                    resolved_path = app_dir / str(custom_tpl)
                    if resolved_path.exists() and resolved_path.is_file():
                        return resolved_path

                    logging.warning(
                        "Custom template '%s' declared in '%s' does not exist in '%s'. "
                        "Falling back to default template.",
                        custom_tpl,
                        md_path.name,
                        app_dir,
                    )
    except Exception as error:
        logging.debug(
            "Stream-based template extraction failed for %s: %s", md_path.name, error
        )

    return default_template


def convert_file(
    md: Path,
    out: Path,
    defaults_yaml: Path,
    template_html: Path,
    lua_filter: Path,
    relative_root: str,
    is_secure: str,
    navigation_menu: list,  # Map the extracted navigation list
    dry_run: bool,
    verbose: bool,
) -> bool:
    """Run pandoc on a single markdown file with dynamic variables. Returns True on success."""
    cmd = [
        "pandoc",
        str(md),
        "--defaults",
        str(defaults_yaml),
        "--template",
        str(template_html),
        "--lua-filter",
        str(lua_filter),
        "-V",
        f"relative_root={relative_root}",
        "-V",
        f"is_secure={is_secure}",
        f"--katex={relative_root}assets/katex/",
        "-o",
        str(out),
    ]

    # Inject list items as repeated variables so Pandoc creates an iterable list array.
    for item in navigation_menu:
        cmd.extend(["-V", f"nav={item}"])

    # Inject relative paths to CSS stylesheets dynamically
    css_files = [
        "assets/css/pico.css",
        "assets/css/custom_002.css",
        "assets/katex/katex.min.css",
    ]
    for css in css_files:
        cmd.extend(["--css", f"{relative_root}{css}"])

    if verbose or dry_run:
        logging.info("  cmd: %s", " ".join(cmd))
    if dry_run:
        return True

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("pandoc failed on %s:\n%s", md, result.stderr.strip())
        return False
    return True


def sync_functional_assets(
    app_assets: Path, dst_assets: Path, dry_run: bool, verbose: bool
):
    """Mirror the functional assets folder (CSS, JS, KaTeX) to the destination assets directory."""
    if not app_assets.exists():
        logging.warning(
            "Functional assets folder not found at: %s — skipping.", app_assets
        )
        return
    if verbose or dry_run:
        logging.info("Syncing functional assets: %s → %s", app_assets, dst_assets)
    if dry_run:
        return
    shutil.copytree(app_assets, dst_assets, dirs_exist_ok=True)
    logging.info("Functional assets synced.")


def sync_media_assets(src_dir: Path, dst_dir: Path, dry_run: bool, verbose: bool):
    """Find and copy all non-markdown files (media, etc.) from SRC to DST, preserving folder structure."""
    if verbose or dry_run:
        logging.info(
            "Syncing media assets (non-markdown files) from %s → %s", src_dir, dst_dir
        )
    if dry_run:
        return

    copied_count = 0
    # Walk through src_dir to find non-markdown files
    for p in src_dir.rglob("*"):
        # Copy files that are not markdown (.md) and not system/hidden files
        if p.is_file() and p.suffix.lower() != ".md" and not p.name.startswith("."):
            rel = p.relative_to(src_dir)
            target = dst_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            copied_count += 1

    if verbose:
        logging.info("Copied %d media asset file(s).", copied_count)


def sync_root_assets(root_src: Path, dst_dir: Path, dry_run: bool, verbose: bool):
    """Copy files from the app root directory (favicon, .htaccess, robots.txt, etc.) directly into DST root."""
    if not root_src.exists():
        logging.warning(
            "App root configuration folder not found at: %s — skipping.", root_src
        )
        return
    if verbose or dry_run:
        logging.info("Syncing root assets: %s → %s", root_src, dst_dir)
    if dry_run:
        return
    shutil.copytree(root_src, dst_dir, dirs_exist_ok=True)
    logging.info("Root assets synced.")


def run_pagefind(site_dir: Path, dry_run: bool, verbose: bool):
    """Run Pagefind indexing on the compiled output directory."""
    if dry_run:
        logging.info("[DRY RUN] Would run Pagefind indexing on: %s", site_dir)
        return

    logging.info("Running Pagefind search indexer...")

    cmd = ["pagefind", "--site", str(site_dir)]

    if verbose:
        logging.info("  cmd: %s", " ".join(cmd))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            logging.error(
                "Pagefind indexing failed (Exit code %d).\n"
                "Ensure pagefind is installed.\n"
                "Stderr:\n%s",
                result.returncode,
                result.stderr.strip(),
            )
        else:
            if verbose and result.stdout:
                logging.info("Pagefind Output:\n%s", result.stdout.strip())
            logging.info("Pagefind indexing completed successfully.")

    except Exception as error:
        logging.error("An unexpected error occurred executing Pagefind: %s", error)


def encrypt_file(
    file_path: Path,
    password: str,
    remember_days: str,
    dry_run: bool,
    verbose: bool,
    template_title: str = None,
) -> bool:
    """
    Encrypts a single HTML file in-place using StatiCrypt.
    Uses .staticrypt.json in the project working directory to maintain consistent salts.
    """
    if not file_path.exists():
        logging.warning("File '%s' not found to encrypt.", file_path)
        return False

    logging.info("Encrypting file: %s", file_path)
    is_windows = sys.platform.startswith("win")

    # Inject the password directly into the running process's environment space.
    os.environ["STATICRYPT_PASSWORD"] = password

    # Convert paths to POSIX style to prevent escape-character conflicts on Windows.
    # Specify the file's parent as the target output directory to achieve in-place encryption.
    cmd = [
        "staticrypt",
        file_path.as_posix(),
        "-d",
        file_path.parent.as_posix(),
        "--config",
        STATICRYPT_CONFIG.as_posix(),
        "--short",
    ]

    if template_title:
        cmd.extend(["--template-title", template_title])

    if remember_days:
        cmd.extend(["--remember", str(remember_days)])

    if verbose or dry_run:
        logging.info("  cmd: %s", " ".join(cmd))
        logging.info(
            "  [StatiCrypt uses secure environment variable for raw password passing]"
        )

    if dry_run:
        return True

    try:
        # Explicitly passing env=os.environ guarantees environment variable propagation on Windows.
        result = subprocess.run(
            cmd, capture_output=True, text=True, shell=is_windows, env=os.environ
        )
        if result.returncode != 0:
            logging.error(
                "StatiCrypt failed on file %s (Exit code %d).\nStderr:\n%s",
                file_path,
                result.returncode,
                result.stderr.strip(),
            )
            return False
        else:
            if verbose and result.stdout:
                logging.info("StatiCrypt Output:\n%s", result.stdout.strip())
            logging.info("Successfully encrypted file: %s", file_path)
            return True
    except Exception as error:
        logging.error("An unexpected error occurred during encryption: %s", error)
        return False


def encrypt_secure_directories(
    dst_dir: Path,
    dir_name: str,
    password: str,
    remember_days: str,
    dry_run: bool,
    verbose: bool,
    template_title: str = None,
) -> bool:
    """
    Finds all subdirectories named 'dir_name' and recursively encrypts their HTML contents in-place.
    Uses .staticrypt.json in the project working directory to maintain consistent salts.
    """
    secure_dirs = [
        p
        for p in dst_dir.rglob("*")
        if p.is_dir() and p.name.lower() == dir_name.lower()
    ]

    if not secure_dirs:
        logging.info("No subdirectories titled '%s' found to encrypt.", dir_name)
        return True

    logging.info(
        "Processing %d '%s' directory/directories for client-side encryption...",
        len(secure_dirs),
        dir_name,
    )

    success = True
    is_windows = sys.platform.startswith("win")

    # Inject the password directly into the running process's environment space.
    os.environ["STATICRYPT_PASSWORD"] = password

    for s_dir in secure_dirs:
        logging.info("Encrypting folder recursively: %s", s_dir.relative_to(dst_dir))

        # Convert paths to POSIX style (forward slashes) to prevent escape-character conflicts on Windows.
        # Add the '--short' flag to suppress the interactive [y/N] prompt on short passwords.
        cmd = [
            "staticrypt",
            s_dir.as_posix(),
            "-r",
            "-d",
            s_dir.parent.as_posix(),
            "--config",
            STATICRYPT_CONFIG.as_posix(),
            "--short",
        ]

        if template_title:
            cmd.extend(["--template-title", template_title])

        if remember_days:
            cmd.extend(["--remember", str(remember_days)])

        if verbose or dry_run:
            logging.info("  cmd: %s", " ".join(cmd))
            logging.info(
                "  [StatiCrypt uses secure environment variable for raw password passing]"
            )

        if dry_run:
            continue

        try:
            # Explicitly passing env=os.environ guarantees environment variable propagation on Windows.
            result = subprocess.run(
                cmd, capture_output=True, text=True, shell=is_windows, env=os.environ
            )
            if result.returncode != 0:
                logging.error(
                    "StatiCrypt failed on %s (Exit code %d).\nStderr:\n%s",
                    s_dir,
                    result.returncode,
                    result.stderr.strip(),
                )
                success = False
            else:
                if verbose and result.stdout:
                    logging.info("StatiCrypt Output:\n%s", result.stdout.strip())
                logging.info(
                    "Successfully encrypted directory: %s", s_dir.relative_to(dst_dir)
                )
        except Exception as error:
            logging.error("An unexpected error occurred during encryption: %s", error)
            success = False

    return success


def main():
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    # Validate configuration and assets path dependencies
    for label, path in [
        ("SRC", SRC),
        ("DEFAULTS_YAML", DEFAULTS_YAML),
        ("TEMPLATE_HTML", TEMPLATE_HTML),
        ("LUA_FILTER", LUA_FILTER),
    ]:
        if not path.exists():
            logging.error("Config path not found (%s): %s", label, path)
            sys.exit(1)

    DST.mkdir(parents=True, exist_ok=True)

    # Collect all .md files (all assets folders inside SRC have been migrated)
    md_files = list(SRC.rglob("*.md"))

    if not md_files:
        logging.warning("No .md files found under %s", SRC)
        sys.exit(0)

    total = len(md_files)
    built = failed = 0

    for md in sorted(md_files):
        rel = md.relative_to(SRC)
        out = DST / rel.with_suffix(".html")

        # Determine if the file resides in any secure directory path or is the special file
        is_secure_file = rel.as_posix() == "qsjwbuf/20260602080508.md"
        is_secure_dir = any(p in ["secure", "secure_guest"] for p in rel.parts)
        is_secure = "true" if (is_secure_dir or is_secure_file) else ""

        # Determine relative root based on path depth
        rel_parent = rel.parent
        depth = len(rel_parent.parts) if rel_parent != Path(".") else 0
        relative_root = "../" * depth if depth > 0 else "./"

        out.parent.mkdir(parents=True, exist_ok=True)
        logging.info("BUILD: %s → %s", rel, out.relative_to(DST))

        # Dynamically resolve template path using high-performance stream parsing
        current_template = extract_custom_template_stream(md, app_dir, TEMPLATE_HTML)

        ok = convert_file(
            md=md,
            out=out,
            defaults_yaml=DEFAULTS_YAML,
            template_html=current_template,
            lua_filter=LUA_FILTER,
            relative_root=relative_root,
            is_secure=is_secure,
            navigation_menu=NAVIGATION_MENU,  # Passing list
            dry_run=args.dry_run,
            verbose=args.verbose,
        )

        if ok:
            built += 1
        else:
            failed += 1

    # 1. Sync functional assets (CSS, JS, Katex) from app/assets to dst/assets
    sync_functional_assets(
        app_dir / "assets", DST / "assets", dry_run=args.dry_run, verbose=args.verbose
    )

    # 2. Sync media assets (non-markdown files) from SRC to DST
    sync_media_assets(SRC, DST, dry_run=args.dry_run, verbose=args.verbose)

    # 3. Sync root assets (favicon, robots.txt, .htaccess, etc.) from app/root to DST root
    sync_root_assets(app_dir / "root", DST, dry_run=args.dry_run, verbose=args.verbose)

    # Run Pagefind Indexer on raw unencrypted text (if no build failures occur)
    if not failed:
        run_pagefind(DST, dry_run=args.dry_run, verbose=args.verbose)

    # Detect the presence of target secure directories in the build destination
    has_personal = any(
        p.is_dir() and p.name.lower() == "secure" for p in DST.rglob("*")
    )
    has_guest = any(
        p.is_dir() and p.name.lower() == "secure_guest" for p in DST.rglob("*")
    )

    # Detect existence of the designated special file
    special_file = DST / "qsjwbuf" / "20260602080508.html"
    has_special = special_file.exists() and special_file.is_file()

    encryption_ok = True

    if (has_personal or has_guest or has_special) and not failed:
        remember_days = cfg.get("metadata", {}).get("remember_days", None)

        # 1. Process 'secure' Personal Folders and designated special file
        if has_personal or has_special:
            if args.dry_run:
                if has_personal:
                    logging.info(
                        "[DRY RUN] Would retrieve personal password from config and encrypt 'secure' folders."
                    )
                if has_special:
                    logging.info(
                        "[DRY RUN] Would retrieve personal password from config and encrypt special file: %s",
                        special_file,
                    )
            else:
                password_personal = os.environ.get("STATICRYPT_PASSWORD_PERSONAL")
                if not password_personal:
                    logging.error(
                        "StatiCrypt personal password not found in environment variable 'STATICRYPT_PASSWORD_PERSONAL'."
                    )
                    sys.exit(1)

                if has_personal:
                    ok = encrypt_secure_directories(
                        dst_dir=DST,
                        dir_name="secure",
                        password=password_personal,
                        remember_days=remember_days,
                        dry_run=args.dry_run,
                        verbose=args.verbose,
                        template_title="Personal Password",
                    )
                    encryption_ok = encryption_ok and ok

                if has_special:
                    ok = encrypt_file(
                        file_path=special_file,
                        password=password_personal,
                        remember_days=remember_days,
                        dry_run=args.dry_run,
                        verbose=args.verbose,
                        template_title="Personal Password",
                    )
                    encryption_ok = encryption_ok and ok

        # 2. Process 'secure_guest' Guest Folders
        if has_guest:
            if args.dry_run:
                logging.info(
                    "[DRY RUN] Would retrieve guest password from config and encrypt 'secure_guest' folders."
                )
            else:
                # Replace the existing password_guest assignment with:
                password_guest = os.environ.get("STATICRYPT_PASSWORD_GUEST")
                if not password_guest:
                    logging.error(
                        "StatiCrypt guest password not found in environment variable 'STATICRYPT_PASSWORD_GUEST'."
                    )
                    sys.exit(1)

                ok = encrypt_secure_directories(
                    dst_dir=DST,
                    dir_name="secure_guest",
                    password=password_guest,
                    remember_days=remember_days,
                    dry_run=args.dry_run,
                    verbose=args.verbose,
                    template_title="Guest Password",
                )
                encryption_ok = encryption_ok and ok

    # Summary
    mode = "[DRY RUN] " if args.dry_run else ""
    logging.info(
        "%sDone. %d/%d built, %d failed.",
        mode,
        built,
        total,
        failed,
    )
    if failed or not encryption_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

***

**config.yaml**

```yaml
# All paths are relative to the project root (~/dev/ticker_tape/)
paths:
  app: "build"
  src: "content"
  dst: "dist"

# assets_dir: directory name for subfolders containing media(images, etc.), css, and js files.
# remember_days: number of days to remember StatiCrypt decryption password in browser cache.
metadata:
  assets_dir: "assets"
  remember_days: 0

# each item in this list will be added as a link to the global navigation menu of the static
# site. they will be added to the menu in the order they are presented here.
navigation_menu:
  - Bookmarks
  - Reminders
```

***

**translate_links.lua**

```lua
function Link(el)
  -- ONLY process links that end in .md AND do NOT start with http
  if el.target:match("%.md(%#?.*)$") and not el.target:match("^http") then
    -- 1. Replace .md with .html
    local new_target = el.target:gsub("%.md", ".html")
    
    el.target = new_target
  end
  return el
end
```

***

**pandoc_md_to_static_html.yaml**

```yaml
reader: markdown
writer: html
embed-resources: false
variables:
  document-css: false
filters:
  - citeproc
top-level-division: chapter
wrap: none
columns: 78
dpi: 72
toc: false
toc-depth: 2
number-sections: false
section-divs: true
identifier-prefix: ""
title-prefix: ""
eol: lf
strip-comments: false
ascii: false
default-image-extension: .jpg
tab-stop: 4
preserve-tabs: false
html-q-tags: false
fail-if-warnings: false
```

***

**pyproject.toml**

*Note: Ignore the python version, the user will manage.*

```toml
[project]
name = "jmbsquared_github"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = "3.12"
dependencies = [
    "pyyaml>=6.0.3",
]
```

***

**md_to_static_html.html**

```html
<!doctype html>
<html
    data-theme="light"
    xmlns="http://www.w3.org/1999/xhtml"
    $if(lang)$
    lang="$lang$"
    xml:lang="$lang$"
    $endif$$if(dir)$
    dir="$dir$"
    $endif$
>
    <head>
        <meta charset="utf-8" />
        <meta name="generator" content="pandoc" />
        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0, user-scalable=yes"
        />

        $for(author-meta)$
        <meta name="author" content="$author-meta$" />
        $endfor$ $if(date-meta)$
        <meta name="dcterms.date" content="$date-meta$" />
        $endif$ $if(keywords)$
        <meta
            name="keywords"
            content="$for(keywords)$$keywords$$sep$, $endfor$"
        />
        $endif$ $if(description-meta)$
        <meta name="description" content="$description-meta$" />
        $endif$

        <title>$if(title-prefix)$$title-prefix$ – $endif$$pagetitle$</title>

        <!-- Portable Asset Resolution using relative_root -->
        <link
            rel="icon"
            type="image/x-icon"
            href="$relative_root$favicon.ico"
        />
        <link
            rel="icon"
            type="image/svg+xml"
            href="$relative_root$favicon.svg"
        />
        <link
            rel="icon"
            type="image/png"
            sizes="96x96"
            href="$relative_root$favicon-96x96.png"
        />
        <link
            rel="apple-touch-icon"
            href="$relative_root$apple-touch-icon.png"
        />
        <link rel="manifest" href="$relative_root$site.webmanifest" />

        $for(css)$
        <link rel="stylesheet" href="$css$" />
        $endfor$

        <script
            src="$relative_root$assets/js/pico_pagefind.js"
            type="module"
        ></script>

        $for(header-includes)$ $header-includes$ $endfor$ $if(math)$ $math$
        $endif$
    </head>

    <body>
        <header class="container site_header">
            <nav>
                <ul>
                    <li>
                        <span class="brand_text"
                            ><a
                                href="https://jmbsquared.com"
                                style="text-decoration: none"
                                >JmB²</a
                            ></span
                        >
                    </li>
                </ul>
                <ul>
                    <li>
                        <a href="$relative_root$index.html" data-tooltip="Home">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="lucide lucide-house-icon lucide-house"
                            >
                                <path
                                    d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"
                                />
                                <path
                                    d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"
                                />
                            </svg>
                        </a>
                    </li>
                    <li>
                        <a href="#" id="open-search" data-tooltip="Search">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                class="lucide lucide-search-icon lucide-search"
                            >
                                <path d="m21 21-4.34-4.34" />
                                <circle cx="11" cy="11" r="8" />
                            </svg>
                        </a>
                    </li>
                    <li>
                        <details class="dropdown">
                            <summary role="button">Menu</summary>
                            <ul>
                                <li>
                                    <a
                                        href="$relative_root$qsjwbuf/20260602080508.html"
                                        data-tooltip="Private"
                                    >
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            width="24"
                                            height="24"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            stroke-width="2"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            class="lucide lucide-lock-keyhole-icon lucide-lock-keyhole"
                                        >
                                            <circle cx="12" cy="16" r="1" />
                                            <rect
                                                x="3"
                                                y="10"
                                                width="18"
                                                height="12"
                                                rx="2"
                                            />
                                            <path
                                                d="M7 10V7a5 5 0 0 1 10 0v3"
                                            />
                                        </svg>
                                    </a>
                                </li>
                                $for(nav)$
                                <li>
                                    <a href="$relative_root$$nav$.html"
                                        >$nav$</a
                                    >
                                </li>
                                $endfor$
                            </ul>
                        </details>
                    </li>
                </ul>
            </nav>
            <hr />

            $for(include-before)$ $include-before$ $endfor$
        </header>

        <main>
            <div class="container">
                <div style="display: none">
                    $if(title)$
                    <span data-pagefind-body data-pagefind-meta="title">
                        $title$
                    </span>
                    $endif$ $if(keywords)$
                    <span data-pagefind-body data-pagefind-meta="keywords">
                        $for(keywords)$$keywords$$sep$, $endfor$
                    </span>
                    $endif$
                </div>

                $if(title)$
                <header id="title-block-header">
                    <h1 class="title">$title$</h1>

                    $if(subtitle)$
                    <p class="subtitle">$subtitle$</p>
                    $endif$ $if(date)$
                    <p class="date">$date$</p>
                    $endif$ $if(abstract)$
                    <div class="abstract">$abstract$</div>
                    $endif$
                    <hr />
                </header>
                $endif$ $if(toc)$
                <nav id="$idprefix$TOC" role="doc-toc">
                    $if(toc-title)$
                    <h2 id="$idprefix$toc-title">$toc-title$</h2>
                    $endif$ $table-of-contents$
                </nav>
                $endif$ $body$
            </div>
        </main>

        <footer class="container">
            <hr />
            <div class="grid">
                <div>$for(keywords)$$keywords$$sep$, $endfor$</div>
                <div style="text-align: right">
                    $for(author)$
                    <p class="author">$author$</p>
                    $endfor$
                </div>
            </div>

            $for(include-after)$ $include-after$ $endfor$
        </footer>

        <dialog id="search-modal">
            <article style="width: 100%; max-width: 600px">
                <header>
                    <button
                        aria-label="Close"
                        rel="prev"
                        id="close-search"
                    ></button>
                    <strong>Search Titles & Keywords</strong>
                </header>
                <input
                    type="search"
                    id="search-input"
                    placeholder="Type to search..."
                    autocomplete="off"
                />
                <ul
                    id="search-results"
                    style="list-style: none; padding-left: 0; margin-top: 1rem"
                ></ul>
            </article>
        </dialog>
    </body>
</html>
```

***

**.gitignore**

```
dist/
*.html
*.log

.DS_Store
Thumbs.db

# Python-generated files
__pycache__/
*.py[oc]
wheels/
*.egg-info

# Virtual environments
.venv
```

***

**.staticrypt.json**

```json
{
    "salt": "081e9265164557e70062a127ba87c806"
}
```

***

name: Build and Deploy Site

on:
  push:
    branches: ["main"] # Trigger on push to main branch
  workflow_dispatch:    # Allow manual trigger

# Set permissions for GitHub Pages deployment

**build.yml**

```yaml
permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install System Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y pandoc

      - name: Install Node Dependencies
        run: |
          npm install -g pagefind staticrypt

      - name: Install Python Dependencies
        run: |
          pip install pyyaml

      - name: Execute Build Pipeline
        run: python build/build_site.py
        env:
          # Mapping GitHub Secrets to the environment variables expected by build_site.py
          STATICRYPT_PASSWORD_PERSONAL: ${{ secrets.STATICRYPT_PASSWORD_PERSONAL }}
          STATICRYPT_PASSWORD_GUEST: ${{ secrets.STATICRYPT_PASSWORD_GUEST }}

      - name: Upload Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist # Upload the output directory

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

***

# 5.

Github secrets were configured. The local system (Linux) has not interacted with the repository at all, and I will need assistance in execution, if no further changes or investigations are needed at this time.
