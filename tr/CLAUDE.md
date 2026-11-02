# Genel Kurallar

<!-- Made By FALCREB -->

## Dil Tercihi
- README.md ve kod içi yorumlar Türkçe yazılsın
- Commit mesajları İngilizce kalsın (conventional commits formatında)

## İletişim
- Benimle Türkçe konuş
- Yazılımcı değilim: konuları sade, gerektiğinde günlük hayattan
  benzetmelerle anlat ki konuyu anlayabileyim
- Ama terimlerden kaçma: alanın gerçek terimlerini kullan (commit, branch,
  merge, dependency, deploy vb.) ve bir terim konuşmada ilk geçtiğinde
  kısaca tanımla — örn. "merge (birleştirme): bir branch'teki
  değişikliklerin ana projeye işlenmesi". Amaç hem konuyu anlamam hem de
  terimleri öğrenmem; anlatım benim için bir eğitim gibi olsun
- Aynı terimi her seferinde baştan tanımlama; ilk geçtiği yerde kısa bir
  tanım yeterli

## Paket Yöneticisi
- JS/Node projelerinde varsayılan olarak pnpm kullan
- Farklı bir paket yöneticisiyle başlamış mevcut bir proje varsa, onu değiştirme

## Güvenlik
- API key, şifre, token gibi hassas bilgileri asla kod içine yazma, her zaman .env kullan
- .env dosyasını asla git'e ekleme, her commit öncesi .gitignore'da olduğunu doğrula
- Hassas bilgi olabilecek bir şey bulduğunda: gerçek bir secret olduğundan
  eminsen .env'ye taşı; belirsiz durumlarda (test fixture, örnek/mock değer
  vb.) otomatik değiştirme, bana bildir ve kararı bana bırak
- Yeni bir bağımlılık/kütüphane eklerken bilinen güvenlik açığı olup olmadığını göz önünde bulundur
- Eğer bir secret yanlışlıkla commit edilmişse: sadece yeni bir commit'te silmek yetmez, geçmişte kalır.
  1) İlgili key/token'ı derhal iptal et / rotate et (servis panelinden),
  2) `git filter-repo` veya BFG Repo-Cleaner ile geçmişten temizle,
  3) Force push gerekiyorsa önce bana haber ver ve onay al.

## .env Yönetimi
- .env oluştururken yanında bir .env.example dosyası da oluştur (gerçek değerler olmadan, sadece değişken isimleriyle) — böylece proje başka bir yerde açıldığında hangi değişkenlerin gerektiği belli olur
- .env.example'ı güncel tut: artık kullanılmayan değişkenleri fark edince
  kaldır, zamanla çöplüğe dönmesin

## Satır Sonu Tutarlılığı (.gitattributes)
- İlk yüklemede proje kök dizinine bir .gitattributes dosyası ekle:
  `* text=auto eol=lf`
- Bu, farklı bilgisayarlar arasında CRLF/LF farkından kaynaklanan
  sahte "değişti" görünümlerini engeller

## Oturum Devamlılığı
PROGRESS.md dosyası her /yukle çalıştığında güncellenir ve şu sabit
şablonu takip eder (format tutarlı olsun ki /devam güvenilir okusun):

```
### [Tarih - Hostname]
- **Yapılanlar & Kararlar:**
- **Son Commit:** (hash + mesaj — /yukle işlemi henüz commit atmadan
  önce, o an geçerli olan HEAD yazılır; henüz commit yoksa "ilk yükleme,
  commit yok" yazılır. Az önce atılan commit'in hash'i tahmin edilerek
  yazılmaz, bir sonraki /yukle'de doğal olarak güncellenir)
- **Aktif Branch:**
- **Sıradaki İlk İş (Next Action):**
- **Bilinen Sorunlar / Dikkat Edilmesi Gerekenler:**
```

- Çalışma ortamı: hostname otomatik alınır (`hostname` komutuyla), elle
  değiştirilmez veya uydurulmaz
- Her yeni oturum başında /devam komutuyla PROGRESS.md ve git durumu
  okunup özetlenir (bu komut salt-okunurdur — bkz. /devam tanımı)
- PROGRESS.md git'e dahil edilsin (hassas bilgi içermeyeceği için .gitignore'a girmesin)

## Changelog
- /yukle her çalıştığında (ilk yükleme veya güncelleme), yapılan
  değişiklikleri CHANGELOG.md'nin [Unreleased] bölümüne 1-2 maddelik
  sade Türkçe cümlelerle ekle
- Yeni bir semver tag atıldığında [Unreleased] içeriğini o versiyon
  başlığı altına taşı, [Unreleased] bölümünü boşalt

## Commit Kuralları
- Commit mesajları İngilizce yazılsın
- Conventional commits formatı kullan (feat:, fix:, docs:, chore:, refactor:)
- Commit mesajını benden isteme; yapılan değişikliği (diff) analiz edip
  uygun mesajı kendin üret
- Her commit tek bir mantıksal değişikliği içersin, büyük değişiklikleri parçalara böl
- Claude'un hazırladığı commit'lerdeki `Co-Authored-By: Claude ...` satırı
  korunsun, silinmesin
- Commit kimliği: `git config --global user.name/user.email` tanımlı değilse
  veya e-posta GitHub hesabıma bağlı değilse commit atmadan önce bana bildir
  (gizlilik için GitHub'ın `...@users.noreply.github.com` adresi önerilir)
- Tüm projeler kimliği global ayardan alır: bir projede local
  (`git config --local`) user.name/user.email tanımlıysa commit atmadan
  önce sormadan kaldır ve bana kısaca bildir

## Branch ve Pull Request Akışı
- Branch adlarında prefix standardı kullan: `feature/`, `fix/`, `chore/`, `docs/`
- Her mantıksal iş birimi (bir özellik, bir hata düzeltmesi, bir bakım işi)
  ayrı bir branch'te yapılır ve GitHub'da Pull Request (PR) açılarak main'e
  merge edilir; main'e doğrudan commit atılmaz (/yukle akışı dahil)
- Tek istisna: reponun ilk yüklemesi (henüz main yokken) doğrudan main'e yapılır
- Tüm repolarda default branch GitHub tarafında korumalı ("Protect default
  branch" ruleset'i): doğrudan push, force push ve branch silme engelli,
  değişiklik yalnızca PR ile girer (onay şartı yok, PR'ı kendim merge
  edebilirim). Yeni repo oluşturulduğunda ilk push'tan hemen sonra aynı
  ruleset'i ekle. Private repolarda bu koruma GitHub Pro gerektirir; Pro
  düşerse kural devre dışı kalır, CLAUDE.md'deki PR kuralı yine geçerlidir
- İşler PR sayısını artırmak için yapay olarak bölünmez; her PR gerçek ve
  anlamlı bir değişiklik içerir
- PR başlığı conventional commits formatında İngilizce, açıklaması kısa
  Türkçe yazılır; PR açıklamasına asla secret/şifre/token yazılmaz
- Testler/lint geçtikten sonra PR'ı merge commit yöntemiyle merge et
  (`gh pr merge --merge`). Merge çakışma verirse veya başarısız olursa
  PR'ı açık bırak, dur ve bildir
- Merge edilmiş branch'i (uzak ve local) sil: içeriği main'e işlendiği için
  bu geri dönüşü olmayan bir silme sayılmaz, onay gerekmez. Merge
  edilmemiş branch'leri onaysız silme
- Merge sonrası local main'i yalnızca fast-forward ile güncelle
  (`git fetch` + `git merge --ff-only origin/main`) — amaç az önce merge
  ettiğin PR'ı local'e almaktır. Fast-forward mümkün değilse (main'de
  beklenmedik başka commit'ler varsa) dur ve bana sor

## Push Öncesi Kontrol
- Push etmeden önce kodun çalıştığını/hata vermediğini kontrol et
- Test dosyaları varsa push öncesi çalıştır. Testler başarısız olursa dur
  ve bildir; proje test içermiyorsa (test dosyası yoksa) bu adımı bilgi
  amaçlı belirt ve devam et — ikisini birbirine karıştırma
- Varsa lint/format aracını (eslint, black, prettier vb.) push öncesi çalıştır
- Kullanılmayan/gereksiz dosyaları (log, cache, geçici dosyalar) commit'e dahil etme
- Push'tan önce mutlaka `git fetch` yap ve remote branch'in local'den ileride
  olup olmadığını kontrol et. Remote'da beklenmedik yeni commit'ler varsa
  otomatik rebase/merge/force/pull yapma — durumu bana açıkça anlat ve
  nasıl ilerlemek istediğimi sor. main/master dahil hiçbir branch'te
  otomatik pull yapma (tek istisna: kendi merge ettiğin PR sonrası
  fast-forward güncelleme, bkz. Branch ve Pull Request Akışı)

## Bağımlılıklar
- Yeni bir kütüphane eklerken güncel/aktif bakımı olan bir sürüm seç
- `^` veya `~` işaretleri package.json'da izin verilen sürüm aralığını belirler;
  bunlar güvenlik yamalarını otomatik yüklemez — asıl tekrarlanabilirliği
  lock dosyası (pnpm-lock.yaml, poetry.lock vb.) sağlar, bu yüzden lock
  dosyası **her zaman commit edilsin**
- Güvenlik güncellemesi gerektiğinde bağımlılığı bilinçsizce en son (latest)
  sürüme yükseltme; mevcut major sürümle uyumlu, güvenli bir sürüm tercih et
- Kullanılmayan/import edilmeyen bağımlılıkları fark edince bana haber ver, istersen kaldırmayı öner
- Tüm repolarda Dependabot uyarıları açık. Yeni oluşturulan repolarda da
  aç (`gh api -X PUT repos/<owner>/<repo>/vulnerability-alerts`). Açık
  critical/high uyarılar varsa projede çalışırken bana bildir; düzeltmeyi
  ayrı bir `fix/` branch'i + PR ile, yukarıdaki sürüm kuralına uyarak yap

## .gitignore Yönetimi
- Projede zaten bir .gitignore varsa önce içeriğini incele, mevcut kuralları koru
- Sadece eksik olan standart girişleri ekle (aşağıdaki taban liste), mevcut
  kuralları benim onayım olmadan silme veya değiştirme
- Taban liste: `node_modules/`, `__pycache__/`, `.venv/`, `dist/`, `build/`, `*.log`, `.DS_Store`, `.env`, `.env.*`, `!.env.example`
  (`.env.*` → `.env.local`, `.env.production` gibi varyantları da dışarıda
  tutar; `!.env.example` ise şablon dosyasının git'e girmeye devam etmesini sağlar)

## Versiyonlama
- Önemli bir aşama tamamlandığında (örn. ilk çalışan sürüm, büyük özellik) semver formatında bir git tag oluşturmayı öner (v1.0.0 gibi)
- Tag atılırken kısa bir CHANGELOG girdisi de ekle (ne değişti, birkaç madde)

## Geri Alma
- Riskli bir değişiklik yapmadan önce, çalışma dizininde benim yaptığım
  commit edilmemiş değişiklikler varsa bunları kendi kararınla commit etme
  (örn. "chore: save current state" gibi) — bunlar yarım kalmış bir işim
  olabilir. Gerekirse mevcut durumu korumak için bir branch/tag/commit
  önerebilirsin ama bunun için benden onay al

## Büyük Dosyalar
- 50MB'ı geçen dosyaları repoya eklemeden önce uyar, gerekirse .gitignore'a ekle veya Git LFS öner

## Çalışma Tarzı
- Değişiklik büyükse önce planı kısaca özetle, sonra uygula
- Mevcut testleri geçen ya da çalıştığını bildiğim bir davranışı, açıkça
  istenmedikçe değiştirme. Bir özelliği eklerken/düzeltirken başka çalışan
  bir şeyi bozuyorsan, yapmadan önce bana söyle

## Raporlama
- Her işlem sonunda ne yapıldığını kısa madde madde özetle (uzun log dökme, sadece sonuç)
- Hata olursa net şekilde neyin başarısız olduğunu söyle, sessizce devam etme
- /yukle sonunda git commit / GitHub push / Pull Request adımlarının her
  birinin durumunu ayrı ayrı belirt; biri başarısız olursa "tamamlandı"
  gibi genel bir cümleyle geçiştirme, hangisinin eksik kaldığını açıkça yaz

## Onay Gerektiren İşlemler (Geri Dönüşü Zor/İmkansız)
Aşağıdaki işlemler için her zaman önce onay iste, hiçbirini otomatik yapma:
- Herhangi bir branch'e force push (`--force` veya `--force-with-lease`) — sadece main/master değil, tüm branch'lerde
- Çalışma dizinindeki kayıtsız değişiklikleri silebilecek komutlar: `git reset --hard`, `git clean -fd`, `git checkout .`, `git restore .`
- Mevcut bir .git repository'sinin origin remote URL'sini değiştirme (bkz. GitHub Yükleme bölümü)
- GitHub reposunun görünürlüğünü (public/private) değiştirme
- Repo silme veya başka bir hesaba transfer etme
- Dosya/klasör silme, repo silme (merge edilmiş branch'lerin silinmesi
  hariç, bkz. Branch ve Pull Request Akışı)
- .env veya secrets içeren dosyaları commit etme (bu zaten asla yapılmamalı, onayla da yapılmaz)

## GitHub Yükleme / Güncelleme / Devam
- Bu işlemler için proje bazlı /yukle ve /devam slash komutlarını kullan
- /yukle hem ilk yükleme hem güncelleme senaryosunu tek komutta yönetir
  (proje .git içeriyor mu ve GitHub'da repo var mı kontrolüne göre dallanır);
  $ARGUMENTS boşsa işlemi başlatma, proje/repo adı belirtilmediğini söyle
- .git zaten varsa origin remote'un URL'sini kontrol et; beklediğinden
  farklı bir GitHub repository'sine bağlıysa bunu otomatik değiştirme,
  durumu bana bildir ve onay iste
- /devam tamamen salt-okunurdur: proje dosyalarını, çalışma dizinini veya
  commit geçmişini değiştirmez. `git fetch` yalnızca remote-tracking
  referanslarını güncellemek için yapılabilir (bu bir dosya değişikliği
  değildir), bunun dışında hiçbir git yazma işlemi yapılmaz
