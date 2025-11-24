## Task_In_Work — tabla de lucru curentă

> Acest fișier este pentru **o singură sarcină activă**. După finalizare, concluziile și faptele confirmate merg în `Project_MAP.md`, iar aici se curăță pentru următoarea sarcină.

---

## 1. Sarcina curentă

- **Titlu**: *(de completat)*
- **Context**: *(de completat scurt — de ce facem asta, ce parte din joc atinge)*
- **Fișiere implicate**: de obicei `main.py`, eventual config sau asset‑uri.
- **Criteriu de succes**: *(condiție clară: “Funcționează X în situațiile Y, fără erori în consolă” etc.)*

---

## 2. Plan (P — Plan)

### 2.1 Observații și simptome
- *(notează aici ce vezi în joc, erori în consolă, comportamente ciudate)*

### 2.2 Ipoteze
- H1: *(exemplu: coliziunea cu spike‑uri nu funcționează corect în anumite frame‑uri)*  
- H2: *(exemplu: datele nu se salvează corect în `save.json` la autosave)*  

### 2.3 Planul experimentelor
Scriem pași clari, fiecare cu ce verificăm și ce rezultat așteptăm.

1. **Pas 1** — *(ex.: Reproduc problema în joc, notez exact pașii)*  
2. **Pas 2** — *(ex.: Adaug loguri/print‑uri în zona de cod suspectă)*  
3. **Pas 3** — *(ex.: Rulez jocul, colectez log‑urile, verific dacă ipoteza H1 se confirmă sau nu)*  

---

## 3. Do (D — Execuția experimentelor)

> Aici se notează **ce s-a făcut efectiv**, cu comenzi, modificări și rezultate observate.

### 3.1 Pași executați

- **Pas 1**:  
  - **Ce am făcut**: …  
  - **Rezultat observat**: …  
  - **Fișiere/modificări**: …  

- **Pas 2**:  
  - **Ce am făcut**: …  
  - **Rezultat observat**: …  
  - **Fișiere/modificări**: …  

*(continui după nevoie)*  

---

## 4. Check (C — Fapte confirmate)

> Doar concluzii pe care le-am **verificat prin teste/observații clare**.

- **Fapt 1**: … *(ex.: la coliziune cu spike de tip `spikewood`, frame 3, lungimea scade corect cu 5 segmente)*  
- **Fapt 2**: … *(ex.: `save.json` este creat/actualizat după `save_game_data()` și conține câmpurile X, Y, Z)*  
- **Fapt 3**: …  

---

## 5. Act (A — Soluție și modificări definitive)

### 5.1 Decizie și soluție
- **Soluția aleasă**: … *(descriere clară, de ce această soluție și nu alta)*  
- **Impact**:
  - Cod atins: …  
  - Alte sisteme afectate: … *(de ex. dificultăți, progres, UI etc.)*

### 5.2 Modificări în cod
- Rezumat foarte scurt (nu cod complet, doar ce s-a schimbat logic):
  - ex.: “Mutat logica de coliziune spike într-o funcție separată și corectat condițiile pentru frame‑urile 2 și 3.”

### 5.3 Verificare finală
- Teste rulate manual:  
  - [ ] scenariu 1  
  - [ ] scenariu 2  
  - [ ] scenariu 3  
- Rezultat: *(OK / nu OK; dacă nu OK, ce mai trebuie făcut)*.

---

## 6. Transfer în documentație și închidere sarcină

- **Ce mutăm în `Project_MAP.md`**:
  - Fapt nou 1: …  
  - Fapt nou 2: …  
- **Ce actualizăm în `Roadmap.md`**:
  - Task X.Y marcat ca “Gata” / actualizare status / creare subtask nou.
- **Stare sarcină**:  
  - [ ] În lucru  
  - [ ] Gata — toate criteriile de succes îndeplinite, modificările verificate.  



