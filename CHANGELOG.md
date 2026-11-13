# Changelog

Bu proje [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/) formatını takip eder.

## [Unreleased]

## [1.1.0] - 2026-11-13

### Eklenenler
- Tek komutluk yükleyici (`install.py`): mevcut dosyaları otomatik yedekler, kit'i kopyalar, plugin'leri kurar ve sonucu raporlar. Kurulum sırasında büyük "MADE BY FALCREB" yazısı gösterir.
- Seçilmiş plugin'ler: superpowers, context7, playwright, frontend-design, security-guidance; isteğe bağlı TypeScript/PHP dil sunucuları (sürümleri sabit, yeni sürüm çıkınca bilgi verilir).
- Plugin'leri sonradan Claude Code içinden eşitlemek için `/setup` (Türkçe: `/kurulum`) komutu.

## [1.0.0] - 2026-11-02

### Eklenenler
- Her commit öncesi çalışan gitleaks secret taraması (`scripts/secret_scan.py`).
- İndirilebilir zip paketi: GitHub Releases, kurulum artık `git clone` gerektirmiyor.
- README için gerçek terminal çıktısından üretilmiş demo.
