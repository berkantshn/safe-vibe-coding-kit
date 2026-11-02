# Safe Vibe Coding Kit

A ready-to-use rule set and two slash commands for people who build real projects with [Claude Code](https://claude.com/claude-code) without being software developers. It came out of daily use by an electrical engineer who ships apps, bots and games this way.

**Türkçe açıklama aşağıda.**

## What you get

| File | Purpose |
|---|---|
| `CLAUDE.md` | Global rules: security, commits, branch + pull request flow, reporting, and actions that always need your approval |
| `commands/ship.md` (`yukle.md` in Turkish) | Runs the upload to GitHub, for first upload or update, with secret checks, tests and a PR |
| `commands/resume.md` (`devam.md` in Turkish) | Read-only summary of where you left off, at the start of each session |

Why it helps:

- Secrets stay out of git, with clear steps if one leaks.
- Claude asks before risky actions such as force push, deleting files or changing visibility.
- `PROGRESS.md` lets you continue on another computer.
- Claude explains the terms it uses, so you learn as you build.

## Before and after

Real results from using these rules across my own projects:

| | Before | After |
|---|---|---|
| Direct changes to main | Anything could overwrite the working version | Blocked by GitHub, and changes go through a pull request |
| Security alerts | Nobody was looking: 73 open alerts across 4 projects, 4 of them critical | 70 fixed, 3 reviewed and accepted as low risk, 0 open |
| GitHub contributions | Commit email not linked: 34 shown | Identity rule added and emails linked: over 2,300 shown |
| Changing computers | Trying to remember where I left off | `/resume` summarizes the last work, open PRs and alerts |

This is what the protection looks like when something tries to write directly to main:

```text
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - Changes must be made through a pull request.
 ! [remote rejected] main -> main (push declined due to repository rule violations)
```

## Install

Back up any existing `CLAUDE.md` and commands first, because these commands overwrite files with the same name.

**Windows (PowerShell):**

```powershell
git clone https://github.com/berkantshn/safe-vibe-coding-kit.git
New-Item -ItemType Directory -Force "$HOME\.claude\commands" | Out-Null
Copy-Item safe-vibe-coding-kit\en\CLAUDE.md "$HOME\.claude\CLAUDE.md"
Copy-Item safe-vibe-coding-kit\en\commands\*.md "$HOME\.claude\commands\"
```

**macOS / Linux:**

```bash
git clone https://github.com/berkantshn/safe-vibe-coding-kit.git
mkdir -p ~/.claude/commands
cp safe-vibe-coding-kit/en/CLAUDE.md ~/.claude/CLAUDE.md
cp safe-vibe-coding-kit/en/commands/*.md ~/.claude/commands/
```

You also need [Git](https://git-scm.com/) and the [GitHub CLI](https://cli.github.com/) (`gh auth login`).

## Use

```text
/resume my-project    # start of a session
/ship my-project      # upload your work
```

New repositories are created **private** by default.

## Good to know

- These are instructions for an AI assistant, not a guarantee. Review what it does, especially before publishing anything.
- Protecting the default branch on a private repository needs a paid GitHub plan. The PR rule still works as an instruction without it.

---

## Türkçe

Yazılımcı olmadan [Claude Code](https://claude.com/claude-code) ile gerçek projeler geliştirenler için hazır kural seti ve iki komut. Bu düzen, uygulama, bot ve oyunlarını bu yöntemle geliştiren bir elektrik mühendisinin günlük kullanımından çıktı.

### İçerik

| Dosya | Ne işe yarar |
|---|---|
| `tr/CLAUDE.md` | Genel kurallar: güvenlik, commit, branch + PR akışı, raporlama, onay gerektiren işlemler |
| `tr/commands/yukle.md` | `/yukle`: projeyi GitHub'a yükler veya günceller |
| `tr/commands/devam.md` | `/devam`: kaldığın yeri salt-okunur olarak özetler |

### Önce ve sonra

Bu kuralları kendi projelerimde kullanmanın gerçek sonuçları:

| | Önce | Sonra |
|---|---|---|
| Main'e doğrudan değişiklik | Her şey çalışan sürümün üzerine yazabiliyordu | GitHub engelliyor, değişiklikler PR ile giriyor |
| Güvenlik uyarıları | Bakan yoktu: 4 projede 73 açık uyarı, 4'ü kritik | 70'i düzeltildi, 3'ü incelenip düşük risk olarak kabul edildi, açık uyarı yok |
| GitHub katkı sayısı | Commit e-postası bağlı değildi: 34 görünüyordu | Kimlik kuralı eklendi, e-postalar bağlandı: 2.300'ün üzerinde |
| Bilgisayar değiştirmek | Nerede kaldığımı hatırlamaya çalışıyordum | `/devam` son işi, açık PR'ları ve uyarıları özetliyor |

### Kurulum

Önce mevcut `CLAUDE.md` ve komut dosyalarının yedeğini al; aynı adlı dosyaların üzerine yazılır.

**Windows (PowerShell):**

```powershell
git clone https://github.com/berkantshn/safe-vibe-coding-kit.git
New-Item -ItemType Directory -Force "$HOME\.claude\commands" | Out-Null
Copy-Item safe-vibe-coding-kit\tr\CLAUDE.md "$HOME\.claude\CLAUDE.md"
Copy-Item safe-vibe-coding-kit\tr\commands\*.md "$HOME\.claude\commands\"
```

**macOS / Linux:**

```bash
git clone https://github.com/berkantshn/safe-vibe-coding-kit.git
mkdir -p ~/.claude/commands
cp safe-vibe-coding-kit/tr/CLAUDE.md ~/.claude/CLAUDE.md
cp safe-vibe-coding-kit/tr/commands/*.md ~/.claude/commands/
```

[Git](https://git-scm.com/) ve [GitHub CLI](https://cli.github.com/) (`gh auth login`) gerekir.

### Kullanım

```text
/devam projem    # oturum başında
/yukle projem    # işini yüklemek için
```

Yeni repolar varsayılan olarak **private** açılır. Bunlar bir yapay zekâ asistanına verilen talimatlardır, garanti değildir; özellikle bir şeyi yayınlamadan önce yapılanları kontrol et.

---

## Support

If this project helped you, please give it a ⭐ and [follow me on GitHub](https://github.com/berkantshn) for more.

İşine yaradıysa projeye ⭐ verip [beni GitHub'da takip edebilirsin](https://github.com/berkantshn).

## License

[MIT](LICENSE)

**Made By FALCREB** · [falcreb.com](https://falcreb.com)
