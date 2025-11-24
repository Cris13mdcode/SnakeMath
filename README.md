# MathSnake – proiect de test cu `simple_main.py`

Acest repo conține proiectul jocului **MathSnake**, iar pentru testarea publicării (inclusiv în browser) folosim un exemplu foarte simplu: `simple_main.py`.

## 1. Rulare locală (desktop)

Necesită:
- Python 3.11+ (sau compatibil)
- `pygame`

Instalare dependențe (în PowerShell / CMD):

```bash
pip install pygame
```

Rulare:

```bash
python simple_main.py
```

Se deschide o fereastră în care un pătrat albastru se rotește la tastele săgeți (↑ ↓ ← →), `ESC` închide aplicația.

## 2. Configurație `pygbag` (web)

Fișierul `pygbag.toml` este setat astfel încât:
- `sources = ["simple_main.py"]`
- `entrypoint = "simple_main.py"`

Astfel, build‑ul web va folosi acest exemplu foarte mic pentru testarea publicării.

Build (dacă ai `pygbag` instalat global):

```bash
pygbag .
```

După build, fișierele web vor fi în folderul `build/web`. Acest folder poate fi urcat pe GitHub Pages pentru testare în browser.






