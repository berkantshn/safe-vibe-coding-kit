"$ARGUMENTS" projesinde kaldığım yerden devam edeceğim.

<!-- Made By FALCREB -->

ÖNEMLİ: Bu komut salt-okunurdur. Proje dosyalarını, çalışma dizinini veya
commit geçmişini değiştirmez. `git fetch` yalnızca remote-tracking
referanslarını güncellemek için yapılabilir (dosya sistemini etkilemez,
bu yüzden salt-okunur ilkesini bozmaz); bunun dışında hiçbir git yazma
işlemi (pull, merge, stash, commit vb.) yapılmaz.

1. PROGRESS.md dosyasını oku (varsa), en son tarih/hostname bölümüne bak
2. Aktif branch'i kontrol et
3. Son 3-5 commit'i incele (mesajlarıyla)
4. Working directory temiz mi, commit edilmemiş değişiklik var mı kontrol et
5. `git fetch` yap ve local branch'in remote'a göre durumunu kontrol et
   (geride/ilerde/senkron)
5b. `gh pr list` ile açık PR'ları ve main dışında kalmış (merge edilmemiş)
   branch'leri kontrol et — yarım kalmış bir PR varsa özetle belirt
5c. Açık Dependabot güvenlik uyarılarını önem derecesine göre say
   (`gh api "repos/<owner>/<repo>/dependabot/alerts?state=open&per_page=100"`);
   critical/high varsa paket adı ve yamalı sürümle birlikte özette belirt
6. README.md'ye ve varsa TODO/bilinen hata notlarına göz at
7. PROGRESS.md'de yazan bilgiyle gerçek git durumunu karşılaştır,
   tutarsızlık varsa belirt (örn. PROGRESS.md'deki commit ile HEAD farklıysa)
8. Proje kök dizininde .env dosyası var mı kontrol et; `.env.example` var ama
   `.env` yoksa bunu bildir (bu komut dosya oluşturmaz)

Sonunda şu formatta kısa bir özet ver — uzun log dökme:
- Son çalışma ortamı: [PROGRESS.md'den — hangi bilgisayar, ne zaman]
- En son ne yapıldı: [PROGRESS.md + son commit'lerden özet]
- Şu an proje durumu: [temiz / yarım kalmış değişiklik var / remote ile
  senkron değil / açık PR var / .env eksik vb.]
- Bilinen sorunlar: [PROGRESS.md'deki ilgili bölümden]
- Güvenlik uyarıları: [Dependabot — critical/high/medium/low sayıları;
  yoksa "açık uyarı yok"]
- Bir sonraki iş: [PROGRESS.md'deki "Sıradaki İlk İş" alanını söyle,
  yoksa son commit'lerden mantıklı bir öneri sun]

Eğer git durumu temiz değilse, remote ile senkron değilse veya .env
eksikse, bunları özellikle vurgula ve nasıl ilerlemek istediğimi sor.

Özellikle: local branch remote'un GERİSİNDE ise (GitHub'da senin bu
bilgisayarda görmediğin yeni commit'ler varsa — örn. diğer bilgisayarda
çalışıp push etmişsindir), bunu net bir şekilde belirt ve "GitHub'daki
güncel hali çekmemi ister misin?" diye sor. Onay alırsan `git pull`
çalıştır — ama bu, /devam'ın kendisinin otomatik yaptığı bir şey değil,
senin açık onayınla yapılan ayrı bir adımdır. Onay almadan asla pull
yapma, özellikle çalışma dizininde commit edilmemiş değişikliklerim
varsa (bunlar üzerine yazılabilir, önce onları da sana hatırlat).
