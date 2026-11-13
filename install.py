#!/usr/bin/env python3
"""Safe Vibe Coding Kit installer. Made By FALCREB.

Usage (from the extracted kit folder):
  python install.py                      # asks for language and optional parts
  python install.py --lang tr --lsp no   # no questions (used by Claude)
  python install.py --check              # report only, change nothing

What it does:
  1. Copies the rules (CLAUDE.md), the slash commands and the scripts into
     ~/.claude. Existing files that differ are backed up first to
     ~/.claude/kit-backups/<date-time>/.
  2. Adds the plugin catalogs and installs the plugins in setup/plugins.json.
  3. Optionally installs language servers (TypeScript/PHP code intelligence).
  4. Reports what was already there, what was installed and what failed.

It is safe to run again: anything already in place is left alone. A copy is
kept at ~/.claude/scripts/install.py, so /setup (or /kurulum) can re-sync the
plugins later without the kit folder.

Exit code: 0 = everything in place, 1 = something is missing or failed.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

KIT_DIR = Path(__file__).resolve().parent
CLAUDE_DIR = Path.home() / ".claude"
SCRIPTS_DIR = CLAUDE_DIR / "scripts"
SETTINGS_FILE = SCRIPTS_DIR / "kit_settings.json"
# Kit klasöründen çalışınca setup/plugins.json, kurulu kopyadan çalışınca kit_plugins.json
PLUGINS_FILE = next(
    (p for p in (KIT_DIR / "setup" / "plugins.json", KIT_DIR / "kit_plugins.json") if p.exists()),
    None,
)
FULL_INSTALL = (KIT_DIR / "en" / "CLAUDE.md").exists()

BANNER = r"""
███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗   ██╗
████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝
██╔████╔██║███████║██║  ██║█████╗      ██████╔╝ ╚████╔╝
██║╚██╔╝██║██╔══██║██║  ██║██╔══╝      ██╔══██╗  ╚██╔╝
██║ ╚═╝ ██║██║  ██║██████╔╝███████╗    ██████╔╝   ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═════╝    ╚═╝

███████╗ █████╗ ██╗      ██████╗██████╗ ███████╗██████╗
██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝██╔══██╗
█████╗  ███████║██║     ██║     ██████╔╝█████╗  ██████╔╝
██╔══╝  ██╔══██║██║     ██║     ██╔══██╗██╔══╝  ██╔══██╗
██║     ██║  ██║███████╗╚██████╗██║  ██║███████╗██████╔╝
╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝
"""

PREREQUISITES = {
    "claude": "https://code.claude.com/docs/en/quickstart",
    "git": "https://git-scm.com/downloads",
    "gh": "https://cli.github.com  (gh auth login)",
    "node": "https://nodejs.org  (LTS)",
    "npm": "Node.js",
}

# Ekrana yazılan metinler: kullanıcının seçtiği dilde gösterilir
TEXT = {
    "title": {"en": "Safe Vibe Coding Kit setup", "tr": "Safe Vibe Coding Kit kurulumu"},
    "mode_check": {"en": "Check mode: nothing will be changed.", "tr": "Kontrol modu: hiçbir şey değiştirilmeyecek."},
    "mode_sync": {
        "en": "Kit folder not found next to this script: syncing plugins only.",
        "tr": "Bu script'in yanında kit klasörü yok: sadece plugin'ler eşitleniyor.",
    },
    "ask_lsp": {
        "en": "Do you write TypeScript/JavaScript or PHP? Install code intelligence for them? [y/N]: ",
        "tr": "TypeScript/JavaScript veya PHP ile kod yazıyor musun? Onlar için kod zekâsı kurulsun mu? [e/H]: ",
    },
    "sec_prereq": {"en": "Required programs", "tr": "Gerekli programlar"},
    "sec_files": {"en": "Rules, commands and scripts", "tr": "Kurallar, komutlar ve script'ler"},
    "sec_market": {"en": "Plugin catalogs (marketplaces)", "tr": "Plugin katalogları (marketplace)"},
    "sec_plugins": {"en": "Plugins", "tr": "Plugin'ler"},
    "sec_npm": {"en": "Language servers (npm, global)", "tr": "Dil sunucuları (npm, global)"},
    "sec_git": {"en": "Git identity", "tr": "Git kimliği"},
    "sec_summary": {"en": "Summary", "tr": "Özet"},
    "no_claude": {
        "en": "Without the claude command, plugins cannot be installed. Install Claude Code first.",
        "tr": "claude komutu olmadan plugin kurulamaz. Önce Claude Code'u kur.",
    },
    "no_plugins_file": {"en": "plugins.json not found", "tr": "plugins.json bulunamadı"},
    "backup_at": {"en": "Backups of changed files", "tr": "Değişen dosyaların yedeği"},
    "lsp_skipped": {"en": "optional, not selected", "tr": "isteğe bağlı, seçilmedi"},
    "auto_update": {
        "en": "(Claude Code updates these plugins by itself; when it says so, type /reload-plugins.)",
        "tr": "(Bu plugin'leri Claude Code kendisi günceller; haber verdiğinde /reload-plugins yaz.)",
    },
    "not_via_npm": {
        "en": "command exists but not installed with npm; version not verified",
        "tr": "komut var ama npm ile kurulmamış; sürüm doğrulanamadı",
    },
    "git_missing": {
        "en": "not set. Set your own name and GitHub email: git config --global user.name \"Your Name\" / user.email \"...@users.noreply.github.com\"",
        "tr": "tanımlı değil. Kendi adını ve GitHub e-postanı ayarla: git config --global user.name \"Adın\" / user.email \"...@users.noreply.github.com\"",
    },
    "newer_info": {
        "en": "Newer versions on npm (not upgraded automatically):",
        "tr": "npm'de daha yeni sürümler var (kendiliğinden yükseltilmedi):",
    },
    "major": {"en": "MAJOR VERSION CHANGE, check compatibility", "tr": "ANA SÜRÜM DEĞİŞİYOR, uyumluluğu kontrol et"},
    "problems": {"en": "Some steps are missing or failed:", "tr": "Eksik veya başarısız adımlar var:"},
    "all_ok": {"en": "Everything is in place.", "tr": "Her şey yerinde."},
    "restart": {
        "en": "Restart Claude Code (VS Code: Ctrl+Shift+P > Reload Window) so the changes take effect.",
        "tr": "Değişikliklerin devreye girmesi için Claude Code'u yeniden başlat (VS Code: Ctrl+Shift+P > Reload Window).",
    },
    "next": {
        "en": "Later, run /setup in Claude Code to re-sync the plugins.",
        "tr": "Daha sonra plugin'leri eşitlemek için Claude Code'da /kurulum çalıştır.",
    },
}

# Durum etiketleri
TAG = {
    "ok": {"en": "OK", "tr": "TAMAM"},
    "missing": {"en": "MISSING", "tr": "EKSİK"},
    "added": {"en": "ADDED", "tr": "EKLENDİ"},
    "installed": {"en": "INSTALLED", "tr": "KURULDU"},
    "enabled": {"en": "ENABLED", "tr": "AÇILDI"},
    "disabled": {"en": "DISABLED", "tr": "KAPALI"},
    "copied": {"en": "COPIED", "tr": "KOPYALANDI"},
    "updated": {"en": "UPDATED", "tr": "GÜNCELLENDİ"},
    "differs": {"en": "DIFFERENT", "tr": "FARKLI"},
    "synced": {"en": "SYNCED", "tr": "EŞİTLENDİ"},
    "newer": {"en": "NEWER VERSION", "tr": "YENİ SÜRÜM VAR"},
    "skipped": {"en": "SKIPPED", "tr": "ATLANDI"},
    "warning": {"en": "WARNING", "tr": "UYARI"},
    "error": {"en": "ERROR", "tr": "HATA"},
}
CHANGE_TAGS = {"added", "installed", "enabled", "copied", "updated", "synced"}


def show_banner() -> None:
    """Büyük 'MADE BY FALCREB' yazısı; renk destekleyen terminalde renkli."""
    renkli = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
    if renkli and os.name == "nt":
        os.system("")  # Windows konsolunda ANSI renk kodlarını açar
    try:
        if renkli:
            print("\033[1;36m" + BANNER + "\033[0m")
        else:
            print(BANNER)
    except UnicodeEncodeError:
        print("\n  *** MADE BY FALCREB ***\n")
    print("  falcreb.com\n", flush=True)


def run(cmd: list[str], timeout: int = 300) -> tuple[bool, str]:
    path = shutil.which(cmd[0])
    if not path:
        return False, f"{cmd[0]} not found"
    try:
        result = subprocess.run(
            [path, *cmd[1:]], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"timeout ({timeout}s)"
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def run_json(cmd: list[str]):
    ok, out = run(cmd)
    if not ok:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return None


def npm_global_versions() -> dict[str, str]:
    path = shutil.which("npm")
    if not path:
        return {}
    try:
        # npm ls bazı uyarılarda hata koduyla çıkar ama JSON'u yine basar
        result = subprocess.run(
            [path, "ls", "-g", "--depth=0", "--json"], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=120,
        )
        deps = json.loads(result.stdout or "{}").get("dependencies", {})
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return {}
    return {name: info.get("version", "") for name, info in deps.items()}


def parse_version(v: str) -> tuple[int, ...] | None:
    try:
        return tuple(int(x) for x in v.split("."))
    except ValueError:
        return None


def load_settings() -> dict:
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def ask_yes_no(question: str) -> bool:
    try:
        answer = input(question).strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes", "e", "evet")


def choose_language(arg: str | None, saved: dict) -> str:
    if arg:
        return arg
    if not sys.stdin.isatty():
        return saved.get("lang", "en")
    default = saved.get("lang", "en")
    try:
        answer = input(f"Language / Dil  [1] English  [2] Türkçe  (Enter = {default}): ").strip()
    except EOFError:
        answer = ""
    return {"1": "en", "2": "tr", "en": "en", "tr": "tr"}.get(answer.lower(), default)


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe Vibe Coding Kit installer. Made By FALCREB.")
    parser.add_argument("--lang", choices=["en", "tr"], help="language of the rules and commands")
    parser.add_argument("--lsp", choices=["yes", "no"], help="install TypeScript/PHP language servers")
    parser.add_argument("--check", action="store_true", help="report only, change nothing")
    args = parser.parse_args()

    show_banner()
    saved = load_settings()
    lang = choose_language(args.lang, saved)

    def t(key: str) -> str:
        return TEXT[key][lang]

    if args.lsp:
        want_lsp = args.lsp == "yes"
    elif "lsp" in saved:
        want_lsp = bool(saved["lsp"])
    elif sys.stdin.isatty() and not args.check:
        want_lsp = ask_yes_no(t("ask_lsp"))
    else:
        want_lsp = False

    print(f"== {t('title')}  ({lang}, LSP: {'yes' if want_lsp else 'no'})")
    if args.check:
        print(t("mode_check"))
    if not FULL_INSTALL:
        print(t("mode_sync"))

    problems: list[str] = []
    changes: list[str] = []
    newer: list[str] = []

    def report(tag: str, message: str) -> None:
        if tag in CHANGE_TAGS:
            changes.append(message)
        print(f"  [{TAG[tag][lang]}] {message}", flush=True)

    def section(key: str) -> None:
        print(f"\n== {t(key)}")

    # 1) Gerekli programlar
    section("sec_prereq")
    missing_programs = set()
    for program, where in PREREQUISITES.items():
        if shutil.which(program):
            report("ok", program)
        else:
            missing_programs.add(program)
            report("missing", f"{program} -> {where}")
            problems.append(f"{program}")

    # 2) Dosyalar (sadece kit klasöründen çalışınca)
    if FULL_INSTALL:
        section("sec_files")
        pairs = [(KIT_DIR / lang / "CLAUDE.md", CLAUDE_DIR / "CLAUDE.md")]
        pairs += [(f, CLAUDE_DIR / "commands" / f.name) for f in sorted((KIT_DIR / lang / "commands").glob("*.md"))]
        pairs += [
            (KIT_DIR / "scripts" / "secret_scan.py", SCRIPTS_DIR / "secret_scan.py"),
            (KIT_DIR / "install.py", SCRIPTS_DIR / "install.py"),
        ]
        if PLUGINS_FILE:
            pairs.append((PLUGINS_FILE, SCRIPTS_DIR / "kit_plugins.json"))
        backup_dir = CLAUDE_DIR / "kit-backups" / datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backed_up = False
        for src, dst in pairs:
            name = dst.relative_to(CLAUDE_DIR).as_posix()
            if dst.exists() and dst.read_bytes() == src.read_bytes():
                report("ok", name)
            elif args.check:
                report("differs" if dst.exists() else "missing", name)
                problems.append(name)
            else:
                try:
                    existed = dst.exists()
                    if existed:
                        # Üzerine yazmadan önce mevcut dosyanın yedeğini al
                        target = backup_dir / dst.relative_to(CLAUDE_DIR)
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(dst, target)
                        backed_up = True
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dst)
                    report("updated" if existed else "copied", name)
                except OSError as exc:
                    report("error", f"{name}: {exc}")
                    problems.append(name)
        if backed_up:
            print(f"  {t('backup_at')}: {backup_dir}")

    if not args.check:
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps({"lang": lang, "lsp": want_lsp}, indent=2), encoding="utf-8")

    if not PLUGINS_FILE:
        report("error", t("no_plugins_file"))
        problems.append("plugins.json")
        return finish(t, problems, changes, newer)
    if "claude" in missing_programs:
        print("\n" + t("no_claude"))
        return finish(t, problems, changes, newer)

    config = json.loads(PLUGINS_FILE.read_text(encoding="utf-8"))

    def selected(item: dict) -> bool:
        return item.get("group", "core") == "core" or (item.get("group") == "lsp" and want_lsp)

    # 3) Marketplace'ler
    section("sec_market")
    existing = {m.get("name") for m in (run_json(["claude", "plugin", "marketplace", "list", "--json"]) or [])}
    for market in config["marketplaces"]:
        if market["name"] in existing:
            report("ok", market["name"])
        elif args.check:
            report("missing", market["name"])
            problems.append(market["name"])
        else:
            ok, out = run(["claude", "plugin", "marketplace", "add", market["source"]])
            report("added" if ok else "error", market["name"] if ok else f"{market['name']}: {out[-300:]}")
            if not ok:
                problems.append(market["name"])
    if not args.check:
        run(["claude", "plugin", "marketplace", "update"])

    # 4) Plugin'ler
    section("sec_plugins")
    installed = run_json(["claude", "plugin", "list", "--json"]) or []
    state = {p.get("id"): p for p in installed}
    for plugin in config["plugins"]:
        pid = plugin["id"]
        info = state.get(pid)
        if not selected(plugin):
            if not info:
                report("skipped", f"{pid} ({t('lsp_skipped')})")
            else:
                report("ok", f"{pid} ({info.get('version', '?')})")
            continue
        if info and info.get("enabled", True):
            report("ok", f"{pid} ({info.get('version', '?')})")
        elif info:
            if args.check:
                report("disabled", pid)
                problems.append(pid)
            else:
                ok, out = run(["claude", "plugin", "enable", pid])
                report("enabled" if ok else "error", pid if ok else f"{pid}: {out[-300:]}")
                if not ok:
                    problems.append(pid)
        elif args.check:
            report("missing", pid)
            problems.append(pid)
        else:
            ok, out = run(["claude", "plugin", "install", pid])
            report("installed" if ok else "error", pid if ok else f"{pid}: {out[-300:]}")
            if not ok:
                problems.append(pid)
    print(f"  {t('auto_update')}")

    # 5) npm araçları: sürümler sabit; farklıysa listedeki kurulur, yenisi varsa sadece bilgi verilir
    tools = [tool for tool in config["npm_tools"] if selected(tool)]
    if tools:
        section("sec_npm")
        npm_versions = npm_global_versions()
        for tool in tools:
            package, target = tool["package"], tool["version"]
            label = f"{package}@{target}"
            current = npm_versions.get(package)
            if "npm" in missing_programs:
                report("skipped", f"{label} (npm)")
                problems.append(label)
                continue
            if current == target:
                report("ok", label)
            elif current is None and shutil.which(tool["command"]):
                report("warning", f"{package}: {t('not_via_npm')} ({target})")
            elif args.check:
                report("differs" if current else "missing", f"{package}: {current or '-'} -> {target}")
                problems.append(label)
            else:
                ok, out = run(["npm", "install", "-g", label], timeout=600)
                if ok:
                    report("synced" if current else "installed", f"{package}: {current} -> {target}" if current else label)
                else:
                    report("error", f"{label}: {out[-300:]}")
                    problems.append(label)
            ok, out = run(["npm", "view", package, "version"], timeout=60)
            lines = out.strip().splitlines() if ok else []
            latest = lines[0].strip() if lines else ""
            have, avail = parse_version(target), parse_version(latest)
            if have and avail and avail > have:
                major = f" ({t('major')})" if avail[0] != have[0] else ""
                report("newer", f"{package}: {target} -> {latest}{major}")
                newer.append(f"{package} {target} -> {latest}{major}")

    # 6) Git kimliği: sadece rapor edilir, script hiçbir zaman değiştirmez
    section("sec_git")
    _, name = run(["git", "config", "--global", "user.name"])
    _, email = run(["git", "config", "--global", "user.email"])
    if name and email and "@" in email:
        report("ok", f"{name} <{email}>")
    else:
        report("missing", t("git_missing"))
        problems.append("git identity")

    return finish(t, problems, changes, newer)


def finish(t, problems: list[str], changes: list[str], newer: list[str]) -> int:
    print(f"\n== {t('sec_summary')}")
    if newer:
        print(f"  {t('newer_info')}")
        for line in newer:
            print(f"    * {line}")
    if problems:
        print(f"  {t('problems')}")
        for p in problems:
            print(f"    - {p}")
    else:
        print(f"  {t('all_ok')}")
    if changes:
        print(f"  {t('restart')}")
    print(f"  {t('next')}")
    print("\n  Made By FALCREB · falcreb.com")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
