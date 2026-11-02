#!/usr/bin/env python3
"""Secret scan with gitleaks: git history + staged files.

Usage:     python ~/.claude/scripts/secret_scan.py [project-folder]
Exit code: 0 = clean, 1 = findings, 2 = scan could not run.

gitleaks is downloaded at a pinned version and verified against its official
checksum; a modified file is never run. Findings are masked, so secret values
are not printed. Reviewed false positives go in the project's .gitleaksignore.
"""
import hashlib
import io
import json
import platform
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

SURUM = "8.30.1"
# Değerler gitleaks'in resmi gitleaks_8.30.1_checksums.txt dosyasından alınmıştır.
PAKETLER = {
    ("Windows", "amd64"): ("windows_x64.zip", "d29144deff3a68aa93ced33dddf84b7fdc26070add4aa0f4513094c8332afc4e"),
    ("Linux", "x86_64"): ("linux_x64.tar.gz", "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"),
    ("Darwin", "arm64"): ("darwin_arm64.tar.gz", "b40ab0ae55c505963e365f271a8d3846efbc170aa17f2607f13df610a9aeb6a5"),
    ("Darwin", "x86_64"): ("darwin_x64.tar.gz", "dfe101a4db2255fc85120ac7f3d25e4342c3c20cf749f2c20a18081af1952709"),
}
ARAC_KLASORU = Path.home() / ".claude" / "tools" / f"gitleaks-{SURUM}"


def araci_hazirla() -> Path:
    """gitleaks kurulu değilse indirir, checksum tutmazsa durur."""
    exe = ARAC_KLASORU / ("gitleaks.exe" if platform.system() == "Windows" else "gitleaks")
    if exe.exists():
        return exe
    anahtar = (platform.system(), platform.machine().lower())
    if anahtar not in PAKETLER:
        raise RuntimeError(f"No gitleaks package defined for this platform: {anahtar}")
    ek, beklenen = PAKETLER[anahtar]
    url = f"https://github.com/gitleaks/gitleaks/releases/download/v{SURUM}/gitleaks_{SURUM}_{ek}"
    with urllib.request.urlopen(url, timeout=120) as yanit:
        veri = yanit.read()
    if hashlib.sha256(veri).hexdigest() != beklenen:
        raise RuntimeError("Checksum mismatch, the downloaded file was not run.")
    ARAC_KLASORU.mkdir(parents=True, exist_ok=True)
    if ek.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(veri)) as arsiv:
            exe.write_bytes(arsiv.read(exe.name))
    else:
        with tarfile.open(fileobj=io.BytesIO(veri), mode="r:gz") as arsiv:
            exe.write_bytes(arsiv.extractfile(exe.name).read())
        exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    return exe


def tara(exe: Path, proje: Path, ek_argumanlar: list[str]) -> list[dict]:
    """Tek bir tarama çalıştırır, maskelenmiş bulguları döndürür."""
    with tempfile.TemporaryDirectory() as gecici:
        rapor = Path(gecici) / "rapor.json"
        sonuc = subprocess.run(
            [str(exe), "git", "--redact=100", "--no-banner", "--log-level=error",
             "--report-format=json", f"--report-path={rapor}",
             f"--gitleaks-ignore-path={proje}",
             *ek_argumanlar, str(proje)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        # gitleaks: 0 = temiz, 1 = bulgu var; başka bir kod aracın kendi hatasıdır.
        if sonuc.returncode not in (0, 1):
            raise RuntimeError(f"gitleaks failed: {sonuc.stderr.strip()[:300]}")
        return json.loads(rapor.read_text(encoding="utf-8")) if rapor.exists() else []


def main() -> int:
    # Windows konsolunda Türkçe karakterler bozulmasın.
    sys.stdout.reconfigure(encoding="utf-8")
    proje = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if subprocess.run(["git", "-C", str(proje), "rev-parse", "--git-dir"], capture_output=True).returncode:
        print(f"ERROR: not a git repository: {proje}")
        return 2
    try:
        exe = araci_hazirla()
        bulgular = tara(exe, proje, ["--staged"])
        # İlk yüklemede henüz commit yoktur, geçmiş taraması atlanır.
        commit_var = not subprocess.run(
            ["git", "-C", str(proje), "rev-parse", "--verify", "-q", "HEAD"], capture_output=True
        ).returncode
        if commit_var:
            bulgular += tara(exe, proje, ["--log-opts=--all"])
    except (RuntimeError, OSError) as hata:
        print(f"ERROR: scan could not run: {hata}")
        return 2

    if not bulgular:
        print("Clean: no secrets found.")
        return 0
    print(f"{len(bulgular)} possible secret(s) found (values hidden):")
    for b in bulgular:
        konum = b.get("Commit", "")[:8] or "staged"
        print(f"  {b['RuleID']}  {b['File']}:{b['StartLine']}  ({konum})  id: {b.get('Fingerprint', '')}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
