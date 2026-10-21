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
