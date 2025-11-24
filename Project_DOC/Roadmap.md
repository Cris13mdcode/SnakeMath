## Roadmap proiect `MathSnake`

### 0. Context
- **Proiect**: joc educațional tip Snake cu matematică (`MathSnake` / `SnakyMath`).
- **Tehnologii**: Python, `pygame`, `pygbag` pentru build web.
- **Stare actuală**: joc funcțional, cu dificultăți, XP, coins, skins, badge‑uri și build web existent.

---

## 1. Epics

1. **Gameplay de bază stabil și plăcut**
2. **Progres jucător (XP, monede, badge‑uri, skins)**
3. **Versiune Web stabilă (pygbag)**
4. **UX/UI și accesibilitate**
5. **Calitate cod, monitorizare și mentenanță**

---

## 2. Epic 1 — Gameplay de bază stabil și plăcut

- **Obiectiv**: șarpele, merele, întrebările de matematică, pereții și spike‑urile să funcționeze clar, fără bug‑uri critice.

### Task 1.1 — Verificare/îmbunătățire coliziuni și “Game Over”
- **Descriere**: revizuirea tuturor cazurilor de coliziune (pereți, pereți metalici, spike simplu/spikewood, corp propriu, margini).
- **Rezultat așteptat**:
  - toate coliziunile duc la comportamentul dorit (moarte, scurtare, trecere prin spike‑uri 1–2 etc.);
  - nu există situații de “blocaj” sau bug‑uri vizibile.
- **Stare**: De definit în `Task_In_Work.md` când intră în lucru.

### Task 1.2 — Balansare dificultate (Ușoară / Medie / Greu)
- **Descriere**: ajustarea parametrilor (`max_num`, număr pereți, spike‑uri, power‑ups) astfel încât fiecare dificultate să se simtă corect.
- **Rezultat așteptat**:
  - Ușoară – potrivită pentru copii începători;
  - Medie – provocare moderată;
  - Greu – provocare reală, dar nu imposibilă.

### Task 1.3 — Testare completă power‑ups (speed, magnet, shield, ghost, coins)
- **Descriere**: verificare pentru fiecare power‑up că:
  - se spawnează corect;
  - se activează și expiră corect;
  - efectele (viteză, ghost, shield, coins) se aplică fără bug‑uri.

---

## 3. Epic 2 — Progres jucător (XP, monede, badge‑uri, skins)

- **Obiectiv**: progresul jucătorului să fie clar, persistent și motivațional.

### Task 2.1 — Verificare sistem salvare/încărcare (`save.json`)
- **Descriere**: testarea funcțiilor `save_game_data()` și `load_game_data()` în toate cazurile:
  - fișier existent / inexistent;
  - date corupte / chei lipsă (fallback la valori implicite).

### Task 2.2 — Design curat pentru sistemul de XP și nivele
- **Descriere**: documentarea clară în `Project_MAP` și cod a regulilor:
  - cât XP se dă pentru fiecare acțiune;
  - formula exactă pentru `xp_to_next_level`;
  - bonusuri la level up.

### Task 2.3 — Skins și economie de monede
- **Descriere**: verificarea prețurilor skins și a fluxului de cumpărare:
  - afișarea clară a prețului;
  - blocarea cumpărării dacă nu sunt destule monede;
  - salvarea imediată după achiziție.

---

## 4. Epic 3 — Versiune Web stabilă (pygbag)

- **Obiectiv**: jocul să ruleze corect în browser (desktop + mobil), folosind `pygbag`.

### Task 3.1 — Verificare build web existent
- **Descriere**: testarea build‑ului din `build/web/index.html`:
  - jocul pornește;
  - input‑ul tastatură funcționează;
  - performanța este acceptabilă.

### Task 3.2 — Alinierea setărilor între local și web
- **Descriere**:
  - verificarea rezoluțiilor (960x960 vs 1024x600 în canvas);
  - verificarea versiunilor Python (`pygbag.toml` 3.11 vs index 3.12) și, dacă este cazul, unificarea configurațiilor.

---

## 5. Epic 4 — UX/UI și accesibilitate

- **Obiectiv**: meniuri clare, feedback vizual bun, text lizibil.

### Task 4.1 — Claritate meniuri (Dificultate, Skins, Badges)
- **Descriere**: verificare și eventual redesign ușor al meniurilor:
  - text clar și lizibil;
  - focus/selectare clară la navigare cu tastatura;
  - mesaj clar pentru lipsă coins.

### Task 4.2 — Feedback pentru întrebări matematice
- **Descriere**: îmbunătățirea feedback‑ului la răspuns:
  - feedback vizual/sunet pentru răspuns corect/greșit;
  - eventual timer sau indicator pentru întrebări.

---

## 6. Epic 5 — Calitate cod, monitorizare și mentenanță

- **Obiectiv**: cod mai ușor de întreținut și debug‑at.

### Task 5.1 — Organizare cod în module
- **Descriere**: analiză dacă merită împărțit `main.py` în module (de ex. `ui.py`, `game_logic.py`, `data_store.py`).

### Task 5.2 — Jurnalizare (logging) simplă
- **Descriere**: înlocuirea graduală a `print(...)` critice cu un sistem simplu de logging (ex. `logging` standard), astfel încât să fie mai ușor de urmărit erorile.

---

## 7. Stare și priorități

- **Scurt termen (1–2 sprinturi)**:
  - Task 1.1, 1.3 (gameplay stabil),
  - Task 2.1 (salvare/încărcare),
  - Task 3.1 (test build web).
- **Mediu termen**:
  - Task 2.2, 2.3 (progres și economie),
  - Task 4.1, 4.2 (UX/UI).
- **Lung termen**:
  - Task 3.2, 5.1, 5.2.

Detalierea exactă a pașilor și a verificărilor pentru fiecare Task se va face în `Task_In_Work.md` atunci când acel Task intră în lucru.







