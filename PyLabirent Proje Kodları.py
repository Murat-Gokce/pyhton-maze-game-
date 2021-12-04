# =================INIT====================
import pygame, sys, os.path
sys.setrecursionlimit(10000)
from pygame.locals import *
pygame.init()
oyunSaati = pygame.time.Clock()

# =================DEĞİŞKERNLER====================
# Sabitler
genislik = 24
yukseklik = 20
u = boyut = 30
pencereGen =  genislik * boyut
pencereYuk = yukseklik * boyut

# Labirent 2 boyutlu tam sayı içeren bir dizidir.
labirent = {}

# Labirent değişkenleri ve kullanılacak terimler
asal = [37,73,43,47,2,83,7,89,41,17,67,71,101,97,3,19,61,5,11,23,53,59,29,13,79,31,103]
sayi = [3755,8187,7883,9111,2503,5838,9544,1001,2246,1840,1160,1069,9369,9540,3213]
seviye = 1
hedef = 0
hedefle = 0

# Köşe değerleri- Hedeflerin bulunduğu noktalar
kontrol = [0,0,0]
kontrol2 = [(1, yukseklik-2),(genislik-2, 1),(genislik-2, yukseklik-2)]

# Oyuncu Değişkenleri
skor = 0
seviyeSkor = 0
oyuncux, oyuncuy = 1,1
dakika = 0
saniye = 0
saniyeSeviyesi = 0
saniyeToplam = 0
saniyeAveraj = 0
arayuz = 0
fps = 14
yuksekSkor = 0
eskiSkor = 0
oyuncuİsmi = 'O1'

# Pygame Penceresi
windowSurfaceObj = pygame.display.set_mode((pencereGen,pencereYuk))
updateRect = pygame.Rect(0,0,u,u)

# Renk Değişkenleri
beyaz  = pygame.Color(255,255,255)
siyah = pygame.Color(0,0,0)
kirmizi = pygame.Color(255,0,0)
yesil = pygame.Color(0,255,0)

def minit():
	global seviye, hedef, hedefle
	seviye = 1
	hedef = hedefle = 0
	global skor, seviyeSkor, yuksekSkor, eskiSkor
	skor = seviyeSkor = yuksekSkor = eskiSkor = 0
	global dakika, saniye, saniyeSeviyesi, saniyeToplam, saniyeAveraj
	dakika = saniye = saniyeSeviyesi = saniyeToplam = saniyeAveraj = 0
	global arayuz
	arayuz = 0

# U genişliğinde kareler ızgaramızda (x, y) de c renkli bir kare çizimi
def cizKare(x,y,c):
	global u
	pygame.draw.rect(windowSurfaceObj, c, (x*u, y*u, u, u))

# Oyuncu veya hedefler olmadan labirent duvarları çizimi
def cizLabirent():
	for x in range(0, genislik):
		for y in range(0, yukseklik):
			if labirent[x,y] == 1:
				cizKare(x,y,siyah)

# Puan ekranını güncelleme
def guncelleSkor():
	global skor, seviye, seviyeSkor, oyuncuİsmi
	global dakika, saniye, arayuz, saniyeSeviyesi, saniyeAveraj
	seviyemsj = ' Seviye:'+ str(seviye)+'('+str(hedefle)+')'
	skormsj = ' Skor:'+str(skor)+'~'+str(seviyeSkor)+'Seviye Başına'
	zamanmsj = ' - Zaman:'+str(dakika)+'m'+str(saniye)+'s'
	if( arayuz < 10 ):
		zamanmsj = zamanmsj+'0'
	zamanmsj = zamanmsj+str(arayuz)+'f Şimdi:'+str(saniyeSeviyesi)
	zamanmsj = zamanmsj+'s Averaj: '+str(saniyeAveraj)+'s'
	msj = 'PyLabirent - '+oyuncuİsmi+' - '+seviyemsj+skormsj+zamanmsj
	pygame.display.set_caption(msj)


# Labirent, hedefler ve oyuncu çizimi ve puan ekranını güncelleme
def cizEkran():
	global dakika, saniye, arayuz, saniyeSeviyesi, saniyeToplam
	arayuz += 1
	if(arayuz >= fps):
		saniye += 1
		saniyeSeviyesi += 1
		saniyeToplam += 1
		arayuz = 0
	if(saniye >= 60):
		dakika += 1
		saniye = 0
	guncelleSkor()
	windowSurfaceObj.fill(beyaz)
	cizKare(oyuncux,oyuncuy,kirmizi)
	cizLabirent()
	for i in range(0,3):
		if kontrol[i] == 0:
			cizKare(*kontrol2[i], c=yesil)
	pygame.display.update()


# Oyun genel koordinatının labirent dışında olup olmadığını kontrol etme
def disari(x,y):
	if x<0 or y<0 or x>=genislik or y>=yukseklik:
		return True
	return False

# Oyun genel koordinatının labirentin kenarında olup olmadığını kontrol etme
def kenar (x,y):
	if x == 0 and (y>=0 and y < yukseklik):
		return True
	if x == (genislik-1) and (y>=0 and y < yukseklik):
		return True
	if y == 0 and (x>=0 and x < genislik):
		return True
	if y == (yukseklik-1) and (x>=0 and x < genislik):
		return True
	return False

# Check if a game world coordinate is blocked by wall
def blok(x,y):
	if( x<0 or y<0 or x>=genislik or y>= yukseklik ):
		return True
	if(labirent[x,y] == 1):
		return True
	return False

# Oyunun genel koordinatının duvar tarafından engellenip engellenmediğini kontrol etme
def rekürsifArama(x,y):
	if blok(x,y):
		return
	if labirent[x,y] == 10:
		return
	if not blok(x,y):
		labirent[x,y] = 10
		rekürsifArama(x-1,y)
		rekürsifArama(x+1,y)
		rekürsifArama(x,y-1)
		rekürsifArama(x,y+1)

#  Tüm labirentin erişilebilir olup olmadığını görmek için yinelemeli bir arama başlatma
def rekürsifAramaBaslat(x,y):
	rekürsifArama(x,y)
	rdeger = True						# rdeger= true, aramanın her şeyi ziyaret ettiği anlamına gelir
	for x in range(1, genislik-1):			# İlk satır ve sütunu yoksay
		for y in range(1, yukseklik-1):	#İlk satır ve sütun her zaman duvardır
			if( labirent[x,y] == 0 ):
				rdeger = False		# Aramanın ziyaret etmediği bir şey bulduk
			if( labirent[x,y] == 10 ):
				labirent[x,y] = 0
	return rdeger

# Bir duvar yerleştirir, labirentin hala geçerli olup olmadığını test eder, test başarısız olursa değişikliği geri alır
def dene (x,y):
	if blok(x,y):
		return False
	labirent[x,y] = 1
	if rekürsifAramaBaslat(1,1):
		return True
	labirent[x,y] = 0
	return False

# 2 faktöre bağlı olarak (x, y) 'de bir duvar oluşturmak isteyip istemediğimizi test eder
def yaratHucre(x,y):
	# 2x2 kareler oluşturma:
	if blok(x-1,y) and blok(x-1,y-1) and blok(x,y-1):
		return
	if blok(x+1,y) and blok(x+1,y-1) and blok(x,y-1):
		return
	if blok(x-1,y) and blok(x-1,y+1) and blok(x,y+1):
		return
	if blok(x+1,y) and blok(x+1,y+1) and blok(x,y+1):
		return
	# Labirentin parçalarını  dene fonksiyonu bunu sağlar
	cizKontrol = dene(x,y)
	if cizKontrol:
		cizKare(x,y,siyah)
		pygame.display.update()
	return

# Oyuncunun konumunu ve seviyesini sıfırlar
def resetle():
	global kontrol, oyuncux, oyuncuy, saniyeSeviyesi
	oyuncux = oyuncuy = 1
	saniyeSeviyesi = 0
	kontrol = [0,0,0]

	global kYukari, kSol, kAsagi, kSag
	global kW, kA, kS, kD
	kYukari = kSol = kAsagi = kSag = False
	kW = kA = kS = kD = False

	
# Hedef ve seviyeye göre bir labirent oluştur
def yarat():
	resetle()
	for x in range(0, genislik):
		for y in range(0, yukseklik):
			labirent[x,y] = 0
			if kenar (x,y):
				labirent[x,y] = 1
	cizEkran()
	i = x = y = 0
	global hedef, seviye, hedefle
	hedef = 111 + 3*(seviye-1) + seviye//3 + seviye//5 + hedefle
	n = hedef%15
	rand = {}
	for i in range(0,256):
		if(n>14):
			n=0
		rand[i] = hedef * sayi[n] + i
		for p in range(0, 27):
			rand[i] += i//asal[p]

	i = 0
	while i<255:
		sayilar = rand[i]
		x = sayilar%genislik
		i += 1
		sayilar = rand[i]
		y =sayilar%yukseklik
		i += 1
		yaratHucre(x,y)
	for x in range(1, genislik-1):
		for y in range(1, yukseklik-1):
			yaratHucre(x,y)
			x2 = genislik-1-x
			y2 = yukseklik-1-y
			yaratHucre(x2, y2)
			yaratHucre(x2//2, y2//2)
			bos = 2+seviye%4
			if(x > 3 and (x+(4*y//3))%bos == 0):
				for y3 in range(y, y+yukseklik//3):
					yaratHucre(x, y3)

					
def sonraSeviye():
	global seviye, skor, skorSeviyesi, hedefle, eskiSkor, yuksekSkor 
	global dakika, saniye, saniyeSeviyesi, saniyeToplam, saniyeAveraj
	skor += 1
	if(saniyeSeviyesi < 200):
		skor += (200-saniyeSeviyesi)//10

	saniyeAveraj = saniyeToplam//seviye
	if(saniyeAveraj < 20):
		skor += 20 - saniyeAveraj
	if(saniyeSeviyesi < 20):
		skor += 20 - saniyeSeviyesi
	seviyeSkor = skor//seviye
	if(seviye == 10 and (skor-eskiSkor) > yuksekSkor):
		yuksekSkor = skor-eskiSkor
	eskiSkor = skor
	seviye += 1
	hedefle = 0
	if(oyuncux > 1):
		hedefle += 1
	if(oyuncuy > 1):
		hedefle += 2
	hedefle -= 1
	yazDosya()
	yarat()

# Oyuncuyu (x * birim, y * birim) taşır
# Tüm oyun mantığı bu işlev aracılığıyla yapılır
def hareket(x,y):
	global oyuncux, oyuncuy, skor
	global seviye, saniyeSeviyesi, dakika, saniye
	global kontrol, kontrol2
	oyuncux += x
	oyuncuy += y
	if(blok(oyuncux,oyuncuy)):
		oyuncux -= x
		oyuncuy -= y
		return
	c = (oyuncux,oyuncuy)
	for i in range(0,3):
		if(kontrol2[i] == c and kontrol[i] == 0):
			kontrol[i] = 1
			if(kontrol[0] == 1 and kontrol[1] == 1 and kontrol[2] == 1): 
				sonraSeviye()
				return


# Oyuncuyu klavye girişine göre hareket ettirir
def hareketler():
	if kW or kYukari:
		hareket(0,-1)
	if kA or kSol:
		hareket(-1,0)
	if kS or kAsagi:
		hareket(0,1)
	if kD or kSag:
		hareket(1,0)

# Oyun bittikten sonra çıkmamızı sağlar.
def cikOyun():
	pygame.quit()
	sys.exit()

# Kayıt dosyasını okumamızı sağlar 
def okuDosya():
	if os.path.isfile('Kayıt.txt'):
		f = open('Kayıt.txt', 'r')
		global seviye, skor, seviyeSkor, hedefle, oyuncuİsmi
		global dakika, saniye, arayuz, saniyeToplam, saniyeAveraj
		seviye, skor, dakika, saniye, arayuz , hedefle = map(int, f.readline().split())
		oyuncuİsmi = f.readline()[:-1]
		f.close()
		if(seviye <= 1 or hedefle >= 3):
			print('PyLabirent Hata: Hatalı Kayıt')
			cikOyun()
		saniyeToplam = dakika*60 + saniye
		seviyeSkor = skor//(seviye-1)
		saniyeAveraj = saniyeToplam//(seviye-1)
		if(seviyeSkor > 150 or saniyeAveraj < 3):
			print('PyLabrent Hata: Hatalı Kayıt ')
			cikOyun()

# Kayıt dosyası oluşturmamızı sağlar.
def yazDosya():
	f = open('Kayıt.txt', 'w')
	temp = str(seviye)+' '+str(skor)
	temp = temp+' '+str(dakika)+' '+str(saniye)+' '+str(arayuz)
	temp = temp+' '+str(hedefle)+'\n'
	temp = temp+oyuncuİsmi+'\n'
	f.write(temp)
	f.close()



def pad(s, n):
	while(len(s) < n):
		s = s + ' '
	return s

# En yüksek skorları kayıt eder.
def kayitYuksekSkor():
	global skor, yuksekSkor, seviye, seviyeSkor, dakika, saniye, arayuz, oyuncuİsmi
	f = open('YuksekSkor.txt', 'a')
	etiket = 'Seviye.' + str(seviye) + ' ' + oyuncuİsmi + ': '
	YukseK = ' En İyi = ' + str(yuksekSkor)
	ToplaM = ' Toplam = '+str(skor)
	sbs = ' Seviye Başına Skor = ' + str(seviyeSkor)
	ZamaN = ' Zaman = '+str(dakika)+'d '+str(saniye)+'s '+str(arayuz)+'a'
	etiket = pad(etiket, 26)
	YukseK = pad(YukseK, 14)
	ToplaM = pad(ToplaM, 16)
	sbs = pad(sbs, 12)
	temp = etiket + YukseK + ToplaM + sbs + ZamaN + '\n'
	f.write(temp)
	f.close()
	kayitYSVeri()

# Oyun bittikten sonra en yüksek skoru kayıt altında tutmamızı sağlar
def kayitYSVeri():
	global skor, yuksekSkor, seviye, seviyeSkor, dakika, saniye, arayuz, oyuncuİsmi
	f = open('YSVeri.txt', 'a')

	temp = str(seviye)+' '+str(yuksekSkor)+' '+str(skor)+' '+str(seviyeSkor)+' '
	temp = temp + str(dakika)+' '+str(saniye)+' '+str(arayuz)+' '+oyuncuİsmi+'\n'
	f.write(temp)
	f.close()


# Oyun bittikten sonra girilen ismi sıfırlamaya yarar
def isimAyar():
	global oyuncuİsmi
	bitirYazma = False
	tempİsim = ''
	while(bitirYazma == False):
		olaylar = 0
		for event in pygame.event.get():
			olaylar += 1
			if event.type == QUIT:
				cikOyun()
			elif event.type == KEYDOWN:
				if event.key == K_RETURN:
					bitirYazma = True
				elif event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))
				else:
					tempİsim = tempİsim + event.unicode

		msj = 'İsim Gir: ' + tempİsim
		pygame.display.set_caption(msj)
		oyunSaati.tick(fps)

	oyuncuİsmi = tempİsim

# Kayıt dosyasını yenilememizi sağlar.
def yeniden():
	minit()
	if os.path.isfile('Kayıt.txt'):
		os.remove('Kayıt.txt')
	yarat()
	isimAyar()

# Main:
minit()
okuDosya()
yarat()
if(seviye == 1):
	isimAyar()
while True:
	#Hareket Olayları:
	olaylar = 0
	for event in pygame.event.get():
		olaylar += 1
		if event.type == QUIT:
			cikOyun()
		# Hareket, her tuşa basma olayı için bir kez yapılır
		# Ayrıca tuş basılı tutulursa kare başına bir kez hareket eder
		elif event.type == KEYDOWN:
			if event.key == K_w:
				kW = True
				hareketler()
			if event.key == K_a:
				kA = True
				hareketler()
			if event.key == K_s:
				kS = True
				hareketler()
			if event.key == K_d:
				kD = True
				hareketler()
			if event.key == K_r:
				kayitYuksekSkor()
				yeniden()
			if event.key == K_UP:
				kYukari = True
				hareketler()
			if event.key == K_LEFT:
				kSol = True
				hareketler()
			if event.key == K_DOWN:
				kAsagi = True
				hareketler()
			if event.key == K_RIGHT:
				kSag = True
				hareketler()
			if event.key == K_SPACE:
				okuDosya()
				yarat()
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
		elif event.type == KEYUP:
			if event.key == K_w:
				kW = False
			if event.key == K_a:
				kA = False
			if event.key == K_s:
				kS = False
			if event.key == K_d:
				kD = False
			if event.key == K_UP:
				kYukari = False
			if event.key == K_LEFT:
				kSol = False
			if event.key == K_DOWN:
				kAsagi = False
			if event.key == K_RIGHT:
				kSag = False
	# Çizim sahnesi ve güncelleme penceresi:
	if(olaylar == 0):
		hareketler()		# Tüm oyun mantığı hareketler  fonksiyonu  ile yapılır
	cizEkran()
	oyunSaati.tick(fps)

