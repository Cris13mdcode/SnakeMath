## Arhitectura generală a proiectului `MathSnake`

- **Tip aplicație**: joc 2D tip „Snake” educațional, cu întrebări de matematică, construit cu `pygame`, cu suport pentru rulare locală și build web (pygbag).
- **Punct de intrare**: `main.py` (funcția `main()`), definit și în `pygbag.toml` (`entrypoint = "main.py"`).
- **Mediu de execuție**:
  - Local: Python 3.x cu biblioteca `pygame`.
  - Web: Python 3.12 în browser prin `pygbag` (`build/web/index.html` încarcă `snakegame.apk` și rulează `main.py` din arhivă).
- **Rezoluție joc**:
  - Fereastră joc: `WIDTH = 960`, `HEIGHT = 960`.
  - Celulă grilă: `CELL = 40`, măr (`APPLE_SIZE = 40`).
  - În web-template, canvas-ul are `1024x600`, dar jocul din `main.py` folosește 960x960.

---

## Componente și module

- **Fișiere Python**:
  - `main.py` — implementarea principală a jocului `MathSnake`:
    - Inițializare `pygame`, fereastră, fonturi, textures/sprite‑uri.
    - Lógica jocului (mișcare șarpe, coliziuni, mere, power‑up‑uri, cufere, spike‑uri, pereți, XP, coins, skins).
    - Meniuri: ecran start, meniu principal, meniu dificultate, meniu skins, ecran badges, ecran „Game Over”.
    - Sistem de salvare/încărcare progres în `save.json`.
  - `SnakeMathoriginal.py` — versiune mai veche a jocului, cu aceeași structură de bază (șarpe, XP, coins, skins etc.); nu este folosită de config‑ul `pygbag` (sursele și entrypoint indică doar `main.py`).
- **Config build web**:
  - `pygbag.toml`:
    - `[project] name = "MathSnake"`, `version = "1.0"`.
    - `sources = ["main.py"]`, `entrypoint = "main.py"`.
    - `[python] version = "3.11"` (versiune țintă pentru runtime Python în build).
- **Front‑end web (pygbag template)**:
  - `build/web/index.html`:
    - Încarcă `pythons.js` de la `https://pygame-web.github.io/archives/0.9/`.
    - Descarcă și montează arhiva `snakegame.apk`, unde se află `assets/main.py`.
    - Rulează `main.py` în context pygame‑web, redând pe un `canvas` HTML5.

---

## Resurse și asset‑uri

- **Imagini necesare (sprite‑uri)** — verificate la pornirea jocului (`required_files` în `main.py`):
  - Sprite‑uri șarpe (skin implicit): `snake_head.png`, `snake_body.png`, `Corner.png`, `snake_tail.png`, `snake_toung.png`.
  - Sprite‑uri skin „lime”: `snake_head_lime.png`, `snake_body_lime.png`, `Corner_lime.png`, `snake_tail_lime.png`, `snake_toung_lime.png`.
  - Sprite‑uri skin „poison”: `snake_head_poison.png`, `snake_body_poison.png`, `Corner_poison.png`, `snake_tail_poison.png`, `snake_toung_poison.png`.
  - Măr normal și negativ: `apple.png`, `apple2.png`.
  - Măr de aur: `applegold.png`.
  - Fundal joc și meniu: `game_background.png`, `main-menu.png`, fundal întrebări: `question.png`.
  - UI: `button.png`, `button2.png`, `button_left.png`, `button_right.png`.
  - Pereți: `wall.png`, `wall_metal.png`.
  - Cufere: `chest_closed.png`, `chest_open.png`.
  - Spike‑uri: `spike1.png`–`spike4.png`, `spikewood1.png`–`spikewood4.png`.
  - Coins: `coins.png`.
  - Cifre pentru scor/sumă etc.: `Nr.0.png` – `Nr.9.png`.
  - Capete bucket: `snake_head_bucket.png`, `snake_head_bucket_lime.png`, `snake_head_bucket_poison.png`.
- **Comportament la lipsa fișierelor**:
  - La start, scriptul verifică existența tuturor fișierelor din `required_files`:
    - Dacă un fișier lipsește, afișează un mesaj de eroare în consolă și pe ecran, apoi închide jocul după 5 secunde.
  - La erori de încărcare `pygame.image.load`:
    - Se folosesc sprite‑uri de rezervă (suprafețe colorate simple) pentru toate tipurile de imagini (șarpe, pereți, butoane, coins, cifre, cufere, spike‑uri).

---

## Structura datelor și starea jocului

- **Stare persistentă (fișier `save.json`)**:
  - Chei folosite:
    - `coins` — număr total de monede acumulate.
    - `unlocked_skins` — dicționar `{nume_skin: bool}`; implicit `{"default": true}`.
    - `current_skin` — string, ex. `"default"`, `"lime"`, `"poison"`. Dacă fișierul conține un skin invalid (ex. `"tiger"`), jocul îl resetează la `"default"`.
    - `badges` — dicționar cu progres badges: `"1games"`, `"10games"`, `"25games"`, `"badge5win"`, `"badge15win"`, `"badge25win"`.
    - `games_played` — jocuri începute.
    - `wins` — jocuri câștigate (score > 0).
    - `xp` — experiența curentă.
    - `level` — nivelul jucătorului.
    - `xp_to_next_level` — XP necesar pentru următorul nivel.
  - Funcții:
    - `save_game_data()` — scrie structura de mai sus în `save.json` (JSON text).
    - `load_game_data()` — încarcă `save.json` dacă există, altfel folosește valori implicite.
- **Sisteme de progres**:
  - Coins:
    - +10 coins pentru fiecare răspuns corect la un măr normal.
    - +10 coins pentru răspuns corect la mărul de aur.
    - +20 coins la power‑up „coins”.
    - coins suplimentare din cufere (random 10–90) și bonus +50 la fiecare al 5‑lea cufăr deschis.
  - XP și nivele:
    - `add_xp(amount)` crește `xp`, verifică depășirea pragului `xp_to_next_level`.
    - La level up: `level` crește cu 1, `xp_to_next_level` se recalculază: `100 * 1.2^(level-1)`, jucătorul primește `level * 5` coins bonus și se salvează progresul.
    - Surse XP:
      - +15 XP pentru măr normal rezolvat corect.
      - +25 XP pentru măr de aur rezolvat corect.
      - XP suplimentar la victorie și la obținerea de badges.
  - Badges:
    - `1games`, `10games`, `25games` — pe baza `games_played`.
    - `badge5win`, `badge15win`, `badge25win` — pe baza `wins`; la fiecare badge nou se acordă XP bonus (50/100/200).
- **Dificultăți** (`DIFFICULTIES`):
  - `"Ușoară"`: `max_num = 10`, operații: `["+", "-"]`.
  - `"Medie"`: `max_num = 20`, operații: `["+", "-"]`.
  - `"Greu"`: `max_num = 30`, operații: `["+", "-"]`.
- **Power‑ups**:
  - Tipuri definite în `power_up_types`:
    - `speed` — crește mult viteza șarpelui pe durată (`duration = 300` ticks).
    - `magnet` — atrage mărul spre șarpe (se mută cu o celulă spre cap).
    - `shield` — anulează o coliziune fatală (folosit pentru spikes/walls).
    - `ghost` — permite trecerea prin propriul corp (nu moare la self‑collision).
    - `coins` — „Coin Storm”, acordă monede suplimentare.
  - Stare:
    - `power_ups` — listă de instanțe pe hartă: `(x, y, type, timer)`.
    - `active_power_ups` — timerele active pe tip (`{"speed": int, ...}`).
- **Obstacole și elemente de hartă**:
  - Pereți normali (`walls`) — blocuri care omoară șarpele la coliziune, dar pot fi distruse când `bucket_mode` este activ (cap „bucket”).
  - Pereți metalici (`metal_walls`) — blocuri indestructibile, omoară instant.
  - Spike‑uri (`spikes`) — listă `(x, y, type, frame, timer)`:
    - `type = 'spike'`:
      - frame 2–3: efect `kill` — moarte instant.
      - frame 0–1: șarpele poate trece.
    - `type = 'spikewood'`:
      - frame 2: `damage_3` — reduce lungimea șarpelui cu 3 segmente (minim lăsând cap+cel puțin un segment).
      - frame 3: `damage_5` — reduce lungimea cu 5 segmente.
      - frame 0–1: trecere fără efect.
  - Cufere (`chests`) — listă `(x, y, opened, timer)`:
    - Cuferele apar după ce jucătorul mănâncă un anumit număr de mere (`apples_since_last_chest >= chest_apples_required`), cu condiția să nu existe deja cufere ne-deschise.
    - La deschidere: acordă monede, cresc `chests_opened_count`, la fiecare 5 cufere deschise activează `bucket_mode` și acordă bonus coins; ulterior cufărul trece în stare deschisă pentru câteva cadre și apoi este șters.

---

## Mecanica de joc (flux de bază)

- **Pornire joc**:
  - `main()`:
    - Apelează `load_game_data()` pentru a încărca progresul.
    - Afișează un ecran „Ready to Start”; la apăsarea unei taste/click iese din acest ecran.
    - Intră în `show_menu()` (meniul principal), de unde jucătorul poate:
      - schimba dificultatea (`show_difficulty_menu()`),
      - deschide meniul de skins (`show_skins_menu()`),
      - începe jocul (`Start` → `start_game()`),
      - ieși din aplicație.
- **Rundă de joc (`start_game`)**:
  - Inițializează:
    - poziția șarpelui (2 segmente), direcția inițială spre dreapta;
    - `current_sum = 0`, `score = 0`;
    - numărul maxim pentru mere în funcție de dificultate (`max_num`);
    - plasează primul măr (`apple`) pe o celulă liberă;
    - generează pereți (`walls`) și pereți metalici (`metal_walls`);
    - resetează și inițializează spike‑uri, power‑ups, cufere, timere și efecte vizuale.
  - **Bucla principală**:
    - Citește input tastatură (`W/A/S/D` pentru direcție, `P` pentru pauză).
    - Calculează `proposed_head` (următoarea poziție a capului).
    - Verifică succesiv coliziuni:
      - Margini și chenar interior: moarte instant.
      - Coliziune cu corpul propriu:
        - dacă `ghost` activ: ignoră coliziunea;
        - altfel scurtează șarpele sau moare dacă are un singur segment.
      - Spike‑uri: efect în funcție de `type` și `frame` (kill / damage / trecere).
      - Pereți metalici: moarte instant.
      - Pereți normali:
        - dacă `bucket_mode` activ: distruge peretele și dezactivează `bucket_mode`;
        - altfel: moarte instant.
      - Power‑ups: activează tipul corespunzător și aplică efectele speciale.
      - Cufere: dacă sunt ne-deschise, acordă reward și marchează deschiderea.
    - Gestionează mărul normal (`apple`) și mărul de aur (`gold_apple`):
      - La coliziune cu măr:
        - Apelează `show_math_question(current_sum, abs(apple_number), operation)`:
          - Desenează o întrebare de forma `current_sum (+/-) apple_number = ?`.
          - Afișează 3 opțiuni numerice; jucătorul alege cu `A/D` și confirmă cu Enter.
        - Dacă răspunsul este corect:
          - Actualizează `current_sum` (între 0 și `max_num` sau `max_hard` pentru mărul de aur).
          - Crește `score`, acordă coins și XP.
          - Creează efecte de particule.
          - Poate genera un măr de aur cu probabilitate 10%.
          - Actualizează progresul pentru cufere și poate genera un nou cufăr.
          - Generează următorul măr (`apple`) și operația (`+` sau `-`).
        - Dacă răspunsul este greșit: șarpele nu crește (se elimină ultimul segment).
    - Desen:
      - Fundal, grilă, pereți, spike‑uri, cufere, power‑ups, mere, șarpe (cu skin‑uri și modul „bucket”), efecte de particule.
      - UI: Sumă curentă, lungime șarpe, scor, coins (icon + număr), bara de XP, power‑ups active (nume + timp rămas).
    - Control viteză:
      - Baza vitezei: crește cu lungimea șarpelui până la un maxim (12 ticks).
      - Dacă șarpele este „roșu” (recent lovit) viteza se reduce ușor.
      - Dacă `speed` activ: viteza crește semnificativ.
      - Frame‑rate controlat prin `clock.tick(...)`.
    - Autosave:
      - La fiecare `AUTOSAVE_INTERVAL` ticks (300) se apelează `save_game_data()`.
- **Game Over**:
  - Funcția `game_over(score)`:
    - Dacă `score > 0`, crește `wins`, acordă XP și poate debloca badges de victorie.
    - Afișează un ecran cu opțiunile:
      - „Restart” — relansează `start_game()`.
      - „Enter” / `Esc` / `m` — revine la `main()` și la meniu.

---

## Interfață și control

- **Controale tastatură în joc**:
  - `W/A/S/D` — mișcarea șarpelui (sus/stânga/jos/dreapta).
  - `P` — pauză/continuare joc.
  - În ecranele de meniu și întrebări:
    - `A/D` — navigare stânga/dreapta între opțiuni.
    - `W/S` — navigare sus/jos în liste (de ex. dificultăți).
    - `Enter` — confirmare selecție.
    - `Esc` — întoarcere înapoi (ex. din meniul dificultate sau skins).
- **Interfață vizuală**:
  - Meniu principal cu 4 butoane: „Dificultate”, „Start”, „Skins”, „Ieșire”, aranjate 2x2.
  - Meniu dificultate: listă cu „Ușoară (1-10)”, „Medie (1-20)”, „Greu (1-30)”.
  - Meniu skins:
    - Preview mărit al șarpelui cu skin selectat.
    - Nume skin („Original Snake”, „Lime Snake”, „Poison Snake”).
    - Status: „GRATUIT”, „DEBLOCAT” sau prețul în COINS.
    - Navigare cu `A/D`, cumpărare cu `Enter` dacă sunt suficiente coins.
  - Ecran badges: afișează doar insignele deblocate și un buton „Exit”.

---

## Log‑uri și mesaje de diagnostic

- La pornire:
  - Mesaje în consolă privind verificarea fișierelor imagine și directorul din care sunt încărcate.
  - În caz de lipsă de fișiere: mesaj de eroare cu calea absolută și lista completă de fișiere necesare.
- La încărcare/salvare date:
  - `save_game_data()` — afișează „Date salvate cu succes!” sau eroare cu detalii din excepție.
  - `load_game_data()` — afișează „Date încărcate cu succes!” sau mesaj că fișierul nu există / eroare și revine la valori implicite.
- La activarea power‑up‑urilor:
  - `activate_power_up()` — tipărește în consolă numele power‑up‑ului activat.

---

## Fapte verificate (rezumat)

- Jocul este un `pygame` single‑file (`main.py`) care implementează:
  - mecanici de șarpe pe grilă,
  - sistem de întrebări matematice la fiecare măr,
  - dificultăți multiple,
  - sistem de XP, nivele, coins, skins și badges,
  - obstacole dinamice (spike‑uri animate, cufere, pereți distrugibili și indestructibili),
  - salvare automată și manuală a progresului în `save.json`.
- Build‑ul web folosește `pygbag` (`pygbag.toml`, `build/web/index.html`) pentru a rula același `main.py` în browser, încărcat din `snakegame.apk`.


