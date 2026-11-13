Safe Vibe Coding Kit plugin'lerini bu bilgisayara kur veya eşitle.

<!-- Made By FALCREB -->

1. Cevabına bu banner'ı olduğu gibi, bir kod bloğu içinde göstererek başla:

```text
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
```

2. `~/.claude/scripts/kit_settings.json` yoksa veya içinde `lsp` değeri
   yoksa, TypeScript/JavaScript veya PHP ile kod yazıp yazmadığımı sor (dil
   sunucularının kurulup kurulmayacağını bu belirler). Varsa kayıtlı seçimi
   kullan.
3. Önce hiçbir şeyi değiştirmeden durumu gör:
   `python ~/.claude/scripts/install.py --check --lang tr`
4. Eksik varsa kısaca listele ve kurulumu çalıştır:
   `python ~/.claude/scripts/install.py --lang tr --lsp <yes|no>`
   - "Gerekli programlar"da EKSİK çıkan bir program (node, gh vb.) varsa
     kendin kurma; nereden kurulacağını söyle.
   - Git kimliği EKSİK çıkarsa kendi adım ve GitHub e-postamla nasıl
     ayarlanacağını söyle; değer uydurma.
   - Bir npm aracı için YENİ SÜRÜM VAR çıkarsa sadece bilgi ver, yükseltme.
5. Bir şey kurulduysa Claude Code'u yeniden başlatmamı hatırlat.

Sonunda kısa bir özet ver: neler zaten vardı, neler kuruldu, neler
başarısız oldu / benim yapmam gerekiyor. Uzun log dökme.
