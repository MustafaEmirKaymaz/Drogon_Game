# 🐉 DRAGON SIEGE: ARCANE SKIES
### Python + Pygame Final Project

---

## 📦 Kurulum

```bash
pip install pygame
python main.py
```

Python 3.8+ ve Pygame 2.x gereklidir.
Harici dosya gerektirmez — tüm grafikler kod içinde çizilir.

---

## 🎮 Kontroller

| Tuş | Aksiyon |
|-----|---------|
| WASD / Ok tuşları | Haraket |
| SPACE veya Z | Büyü fırlat |
| 1, 2, 3, 4 | Büyü seç |
| E | Sonraki büyüye geç |
| X veya B | Bomba kullan (ekranı temizler) |
| F5 | Hızlı kaydet |
| P | Oyunu duraklat |
| ESC | Menüye dön |

---

## ✨ Büyüler

| # | Büyü | Mana | Özellik |
|---|------|------|---------|
| 1 | Arcane Bolt | 5 | Hızlı, düşük maliyetli |
| 2 | Fireball | 15 | Yavaş, yüksek hasar |
| 3 | Ice Shard | 10 | Düşmanları deler |
| 4 | Lightning | 20 | Yayılarak deler |

Büyüler **güçlendirme kutularından** açılır!

---

## 🎯 Oynanış

- Ejderhaları yok et → Kill sayacı dolar → **Boss karşına çıkar**
- Boss'u yenersin → Sonraki levela geçersin
- Her level düşmanlar daha hızlı ve daha çok olur
- Boss 3 faza sahiptir (HP azaldıkça hızlanır ve ateş artırır)

## 💊 Güçlendirmeler

| İkon | Etki |
|------|------|
| ❤ HP | +40 Can |
| 💧 Mana | +50 Mana |
| ✨ Büyü | Yeni büyü açar |
| 🛡 Kalkan | 5 sn dokunulmazlık |
| 💣 Bomba | +1 Magic Bomb |

---

## 🗂 Proje Yapısı

```
dragon_mage_shooter/
├── main.py          ← Ana oyun dosyası (tek dosya)
└── savegame.json    ← Otomatik oluşur (save/load)
```

---

## 🏗 Teknik Özellikler

- **~900 satır** temiz, yorumlu Python kodu
- Tüm görseller **programatik olarak çizilir** (Pygame Surface)
- **Sprite tabanlı** OOP mimari
- **State machine** (Menu / Playing / Paused / Boss / LevelClear / GameOver)
- **Particle sistemi** (patlama efektleri)
- **Parallax yıldız arkaplanı** ve kale silueti
- **JSON tabanlı** Save/Load sistemi
- **Boss AI** — 3 fazlı, farklı ateş desenleri
- **Formation Spawner** — 6 farklı düşman formasyonu
- **Büyü sistemi** — 4 kilidini açılabilir büyü

---

*Geliştirildi: Python 3.x + Pygame 2.x*
*Final Projesi — Oyun Programlama*
