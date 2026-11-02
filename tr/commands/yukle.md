"$ARGUMENTS" projesini GitHub'a yükle/güncelle.

<!-- Made By FALCREB -->

Eğer $ARGUMENTS boşsa: işlemi başlatma, proje/repo adının belirtilmediğini
söyle ve dur.

Not: $ARGUMENTS, GitHub'da oluşturulacak/kullanılacak repo adıdır. Mevcut
çalışma dizini proje dosyalarının bulunduğu yerdir — ikisinin adı farklı
olabilir, birbirine karıştırma.

Bu komut GitHub senkronizasyonundan sorumludur ve değişiklikleri
genel kurallardaki "Branch ve Pull Request Akışı"na göre GitHub'a taşır:
ilk yükleme hariç main'e doğrudan commit atılmaz, her güncelleme bir
branch + PR + merge olarak yapılır.

## 0. DURUM TESPİTİ (dallanma noktası)
Önce şunu belirle: bu bir İLK YÜKLEME mi, yoksa GÜNCELLEME mi?
- Proje dizininde .git yoksa → İLK YÜKLEME
- .git varsa ama remote yoksa veya GitHub'da bu isimde repo yoksa → İLK YÜKLEME
- .git var ve GitHub'da repo zaten mevcutsa → GÜNCELLEME

Ek kontrol: .git zaten varsa origin remote'un URL'sini oku. Eğer bu remote
"$ARGUMENTS" ile eşleşmeyen, beklenmedik başka bir GitHub reposuna
bağlıysa DURDUR — remote'u otomatik değiştirme, durumu bana açıkça
anlat ve nasıl ilerlemek istediğimi sor.

Hangi moda girdiğini bana açıkça söyle, sonra ilgili adımları uygula.

---

## İLK YÜKLEME akışı

1. GIT BAŞLATMA
`git init` yap. .git zaten varsa bu adımı atla, yeniden initialize etme.

2. HASSAS BİLGİ TARAMASI
Kod içinde API key, şifre, token gibi hassas bilgi olup olmadığını tara.
- Gerçek bir secret olduğundan eminsen (ör. gerçek servislere ait,
  production formatında bir key/token) .env dosyasına taşı ve ilgili
  kodu güncelle.
- Belirsiz durumlarda (test fixture'ı, örnek/mock değer, "example"/"test"
  içeren isimler vb.) otomatik değiştirme — bana ne bulduğunu ve nerede
  bulduğunu bildir, kararı bana bırak.
- Sadece o an mevcut dosyalara bakma; `git status` ve `git diff --cached`
  ile staged değişiklikleri de kontrol et — bir secret yanlışlıkla stage
  edilmiş ama henüz commit edilmemiş olabilir.

3. .GITIGNORE
Projede zaten bir .gitignore varsa içeriğini incele ve mevcut kuralları
koru. Sadece eksik olan standart girişleri ekle — liste genel
kurallardaki ".gitignore Yönetimi" bölümündeki taban listedir (oradaki
liste esas alınır, burada ayrıca tekrarlanmaz). Mevcut kuralları benim
onayım olmadan silme/değiştirme.

Ek kontrol: daha önce git'e girmiş `.env.*` dosyası (`.env.example`
hariç) varsa yalnızca .gitignore'a eklemek yetmez — bunu bana bildir,
genel kurallardaki "secret yanlışlıkla commit edilmişse" adımları geçerlidir.

4. .GITATTRIBUTES
Kök dizine `.gitattributes` dosyası ekle, içine `* text=auto eol=lf` yaz.
Bu, farklı bilgisayarlar arasında CRLF/LF kaynaklı sahte değişiklikleri
engeller.

5. BÜYÜK DOSYA KONTROLÜ
Commit'e dahil edilecek (staged) dosyalar arasında 50MB'ı geçen var mı
kontrol et — sadece yeni eklenenler değil, daha önce commit edilmiş olup
şimdi değişmiş dosyalar da dahil. Varsa bana haber ver; gerekirse
.gitignore'a ekle veya Git LFS öner, onay almadan commit'e dahil etme.

6. README.md OLUŞTUR (Türkçe)
İçinde: projenin ne işe yaradığı, kurulum adımları, çalıştırma komutları,
kullanılan teknolojiler, varsa ekran görüntüsü/örnek çıktı.

7. PROGRESS.md OLUŞTUR
Genel kurallardaki sabit şablonu kullan:
```
### [Tarih - Hostname]
- **Yapılanlar & Kararlar:**
- **Son Commit:** ilk yükleme, commit yok
- **Aktif Branch:**
- **Sıradaki İlk İş (Next Action):**
- **Bilinen Sorunlar / Dikkat Edilmesi Gerekenler:**
```
Hostname'i `hostname` komutuyla otomatik al, elle değiştirme.

8. CHANGELOG.md OLUŞTUR
"Keep a Changelog" formatında, [Unreleased] başlığı altına ilk sürümün
maddelerini ekle.

9. PAKET YÖNETİCİSİ TESPİTİ
Projenin dilini/yapısını tespit et (package.json → npm/pnpm/yarn,
pyproject.toml/poetry.lock → poetry, requirements.txt → pip, vb.).
JS/Node projesiyse ve henüz bir paket yöneticisi seçilmemişse pnpm kullan.

10. TEST VE LINT KONTROLÜ
Proje içinde test dosyaları veya lint/format aracı (eslint, black,
prettier vb.) varsa çalıştır. Test başarısız olursa dur, net şekilde
söyle. Proje test içermiyorsa (test dosyası yoksa) bunu bilgi amaçlı
belirt ve devam et — ikisini birbirine karıştırma.

11. İLK COMMIT VE GITHUB
(İlk yüklemede henüz main olmadığı için bu commit doğrudan main'e atılır;
PR akışı bir sonraki /yukle'den itibaren geçerlidir.)
- Staged değişikliklerin diff'ini analiz ederek conventional commits
  formatında uygun bir ilk commit mesajı üret (diff'in kendisini bana
  dökme, sadece üretilen commit mesajını göster) ve commit'i at
- GitHub'da "$ARGUMENTS" isimli bir repo var mı kontrol et:
  - Yoksa private repo oluştur
  - Zaten varsa yeni repo oluşturma, mevcut repoyu kullan ve bana bildir
- Push'tan önce fetch yap, sorun yoksa push et
- Reponun "About" kısmına kısa açıklama ve topic etiketleri ekle
- Repoda Dependabot uyarılarını aç
  (`gh api -X PUT repos/<github-kullanıcı-adı>/$ARGUMENTS/vulnerability-alerts`)
- İlk push'tan sonra default branch'e koruma kuralı ekle ("Protect
  default branch" ruleset'i: deletion + non_fast_forward + pull_request,
  onay sayısı 0; hedef `~DEFAULT_BRANCH`):
  `gh api -X POST repos/<github-kullanıcı-adı>/$ARGUMENTS/rulesets --input <ruleset.json>`

---

## GÜNCELLEME akışı

0. YAPI DOSYASI KONTROLÜ (git durumuna bakmadan ÖNCE yapılır)
Proje kök dizininde şu dosyaların var olup olmadığını kontrol et:
README.md, PROGRESS.md, CHANGELOG.md, .gitattributes, .env.example
(eğer .env varsa). Bu proje daha önce (bizim /yukle sistemimiz olmadan)
yüklenmiş olabilir, bu yüzden bu dosyalar eksik olabilir.
- Eksik olan varsa: İLK YÜKLEME akışındaki ilgili adımdaki aynı
  şablon/içerikle oluştur (PROGRESS.md ve CHANGELOG.md standart
  şablonla, .gitattributes `* text=auto eol=lf` ile)
- Hepsi zaten varsa: hiçbir şey yapma, bu adımı atla

Ayrıca GitHub'daki reponun "About" kısmını kontrol et (gh repo view ile
description ve topic'lere bakılabilir). Açıklama ve topic'ler boşsa,
projeye uygun kısa bir açıklama ve birkaç topic etiketi ekle. Bu proje
muhtemelen bizim sistemden önce yüklendiği için bu adım hiç yapılmamış
olabilir.

Bu adım projeyi sisteme "adapte eder" — bir dahaki /yukle çalıştığında
tekrar tekrar kontrol edilmesine gerek kalmaz.

1. DEĞİŞİKLİK KONTROLÜ
(0. adımda dosya oluşturulduysa git durumu artık temiz değildir, bu
normal — devam et.) Git durumu hâlâ temizse ve ne push edilmemiş commit
ne de bu projeye ait açık bir PR varsa bana söyle ve dur — gereksiz
commit oluşturma. Push edilmemiş commit veya açık PR varsa
7. adıma geçip onları tamamla. Değişiklik varsa devam et;
yeni eklenmiş hassas bilgi için İLK YÜKLEME'deki 2. adımdaki aynı
temkinli kuralı uygula.

Riskli bir değişiklik yapacaksan ve çalışma dizininde benim commit
etmediğim değişikliklerim varsa, bunları kendi kararınla commit etme —
yarım kalmış bir işim olabilir. Gerekirse koruma amaçlı bir branch/tag
önerebilirsin ama önce benden onay al.

2. BÜYÜK DOSYA KONTROLÜ
Commit'e dahil edilecek (staged) dosyalar arasında 50MB üstü var mı
kontrol et — sadece yeni/değişen değil, commit'e girecek her şeyi
kapsa. Varsa bana sor.

3. README KONTROLÜ (Türkçe)
Yeni özellik/komut/bağımlılık eklendiyse güncelle.

4. PROGRESS.md GÜNCELLE
Sabit şablonu koru, yeni bir tarih/hostname bölümü ekle:
```
### [Tarih - Hostname]
- **Yapılanlar & Kararlar:** (3-5 madde)
- **Son Commit:** (bu /yukle işlemi commit atmadan ÖNCEKİ HEAD — henüz
  oluşmamış commit'in hash'ini tahmin ederek yazma; yeni commit'in
  hash'i bir sonraki /yukle'de doğal olarak yazılır)
- **Aktif Branch:** (işlem sonunda dönülecek branch — normalde main;
  çalışılan branch ve PR bilgisi "Yapılanlar" içinde geçer)
- **Sıradaki İlk İş (Next Action):**
- **Bilinen Sorunlar / Dikkat Edilmesi Gerekenler:**
```
Hostname'i otomatik al.

5. CHANGELOG.md GÜNCELLE
[Unreleased] bölümüne 1-2 maddelik sade Türkçe cümlelerle ekle. Yeni bir
semver tag atılıyorsa [Unreleased] içeriğini o versiyon başlığına taşı.

6. TEST VE LINT KONTROLÜ
Aynı kural: test başarısızsa dur; test yoksa bilgi ver ve devam et.

7. GIT, PULL REQUEST VE GITHUB
- Branch belirleme:
  - Aktif branch main ise: değişikliğin konusuna uygun prefix'li bir
    branch aç (örn. `feature/giris-ekrani`, `fix/fiyat-hesabi`);
    commit edilmemiş değişiklikler yeni branch'e taşınır
  - Zaten bir feature/fix/chore/docs branch'indeysen onu kullan
  - Çalışma dizinindeki değişiklikler birbirinden bağımsız birden fazla
    konu içeriyorsa, nasıl ayrılacağını bana kısaca sor
- Staged değişikliklerin diff'ini analiz ederek uygun commit mesajını
  üret (diff'in kendisini bana dökme, sadece üretilen mesajı göster) ve
  commit'le
- Push'tan önce `git fetch` yap, remote local'den ileride mi kontrol et.
  Beklenmedik yeni commit'ler varsa otomatik rebase/merge/force/pull
  yapma — durumu anlat, nasıl ilerlemek istediğimi sor
- Sorun yoksa branch'i push et ve PR aç (başlık: conventional commits
  formatında İngilizce; açıklama: kısa Türkçe özet). Bu branch için
  zaten açık bir PR varsa yenisini açma, onu kullan
- 6. adımdaki test/lint geçtiyse PR'ı `gh pr merge --merge` ile merge et.
  Merge başarısız olursa (çakışma vb.) PR'ı açık bırak, dur ve bildir
- Merge sonrası: uzak ve local branch'i sil, main'e geç,
  `git fetch` + `git merge --ff-only origin/main` ile güncelle.
  Fast-forward mümkün değilse dur ve bana sor

---

## SONUÇ RAPORU
Şu adımların her birinin durumunu ayrı ayrı söyle:
- Git commit: başarılı / başarısız
- GitHub push: başarılı / başarısız
- Pull Request: merge edildi / açık kaldı (neden) / başarısız — PR linkiyle
  (ilk yüklemede "ilk yükleme, PR yok")
Biri başarısız olduysa hangisinin başarılı olduğunu ve neyin eksik
kaldığını açıkça yaz. Başarılı olanlar için repo linkini paylaş.
