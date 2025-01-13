# Bist_Takip
Python kullanarak Borsa İstanbul hisselerini takip edebileceğimiz bir program geliştirdim.Bunu yaparken Yahoo Finance Api'ını kullandım.Anasayfada en çok işlem gören hisselerin yanısıra sağ panelde günün en çok yükselen ve en çok düşen hisselerini görebilirsiniz.Bunlara ek olarak istediğiniz iki hisseyi karşılaştırabileceğiniz karşılaştırma modu da mevcut.

I developed a program using Python to track stocks on the Borsa Istanbul. For this, I utilized the Yahoo Finance API. On the main page, you can see the most actively traded stocks, while the right panel displays the top gainers and losers of the day. Additionally, there's a comparison mode where you can compare any two stocks of your choice.


BIST Piyasa Takip Uygulaması - Kurulum ve Çalıştırma Kılavuzu
=================================================
BIST Market Tracking Application - Installation and Usage Guide
=================================================

[TÜRKÇE]
Bu uygulama, BIST (Borsa İstanbul) hisselerini takip etmenizi, detaylı analizler yapmanızı ve hisseleri karşılaştırmanızı sağlar.

1. Python Kurulumu
-----------------
1. https://www.python.org/downloads/ adresine gidin
2. En son Python sürümünü indirin (Python 3.8 veya üstü önerilir)
3. İndirilen kurulum dosyasını çalıştırın
4. Kurulum sırasında "Add Python to PATH" seçeneğini işaretlediğinizden emin olun
5. Kurulumu tamamlayın

2. Gerekli Kütüphanelerin Kurulumu
---------------------------------
1. Windows tuşu + R tuşlarına basın
2. "cmd" yazıp Enter tuşuna basın
3. Açılan komut penceresinde sırasıyla aşağıdaki komutları yazıp Enter tuşuna basın:

pip install customtkinter
pip install yfinance
pip install matplotlib

3. Uygulamayı Çalıştırma
------------------------
1. final.py dosyasının bulunduğu klasöre gidin
2. Boş bir alanda Shift tuşuna basılı tutarak sağ tıklayın
3. "PowerShell penceresini burada aç" seçeneğine tıklayın
4. Açılan pencerede aşağıdaki komutu yazıp Enter tuşuna basın:

python final.py

4. Uygulama Özellikleri
----------------------
- Ana ekranda tüm BIST hisselerinin güncel fiyatları ve değişimleri görüntülenir
- Sağ panelde en çok yükselen ve düşen hisseler listelenir
- Arama kutusu ile istediğiniz hisseyi hızlıca bulabilirsiniz
- Herhangi bir hisseye çift tıklayarak detaylı analiz ekranını açabilirsiniz
- "Hisse Karşılaştır" butonu ile iki hisseyi yan yana analiz edebilirsiniz

5. Sorun Giderme
---------------
Eğer uygulama çalışmazsa:
1. Tüm kütüphanelerin doğru kurulduğundan emin olun
2. Internet bağlantınızı kontrol edin
3. Python'un PATH'e eklendiğinden emin olun
4. Windows PowerShell'de şu komutu çalıştırarak Python sürümünü kontrol edin:
   python --version

6. Sık Karşılaşılan Hatalar
--------------------------
1. "Module not found" hatası:
   - İlgili kütüphaneyi pip install ile yeniden kurun

2. "Permission denied" hatası:
   - PowerShell'i yönetici olarak çalıştırın

3. "Python is not recognized" hatası:
   - Python'u PATH'e ekleyin veya Python'u yeniden kurun

Not: Bu uygulama eğitim amaçlıdır ve finansal tavsiye niteliği taşımaz.

[ENGLISH]
This application allows you to track BIST (Borsa Istanbul) stocks, perform detailed analysis, and compare stocks side by side.

1. Python Installation
--------------------
1. Go to https://www.python.org/downloads/
2. Download the latest Python version (Python 3.8 or higher recommended)
3. Run the downloaded installer
4. Make sure to check "Add Python to PATH" during installation
5. Complete the installation

2. Required Libraries Installation
-------------------------------
1. Press Windows key + R
2. Type "cmd" and press Enter
3. In the opened command prompt, type the following commands and press Enter after each:

pip install customtkinter
pip install yfinance
pip install matplotlib

3. Running the Application
------------------------
1. Navigate to the folder containing final.py
2. Hold Shift and right-click in an empty area
3. Click "Open PowerShell window here"
4. In the opened window, type the following command and press Enter:

python final.py

4. Application Features
---------------------
- View current prices and changes of all BIST stocks on the main screen
- See top gainers and losers in the right panel
- Quickly find any stock using the search box
- Double-click any stock to open detailed analysis screen
- Use "Compare Stocks" button to analyze two stocks side by side

5. Troubleshooting
----------------
If the application doesn't work:
1. Ensure all libraries are properly installed
2. Check your internet connection
3. Make sure Python is added to PATH
4. Check Python version in PowerShell by running:
   python --version

6. Common Errors
--------------
1. "Module not found" error:
   - Reinstall the relevant library using pip install

2. "Permission denied" error:
   - Run PowerShell as administrator

3. "Python is not recognized" error:
   - Add Python to PATH or reinstall Python

7. Updates and Maintenance
------------------------
- Keep the application updated regularly
- Keep libraries up to date:
  pip install --upgrade customtkinter yfinance matplotlib

8. Contact and Support
--------------------
If you encounter any issues or need assistance:
[Add your contact information here]

Note: This application is for educational purposes and does not constitute financial advice. 
