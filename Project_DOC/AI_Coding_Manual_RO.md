# Sistemul de lucru în Cursor

Documentele și procesele de lucru sunt organizate pe principiul „registraturii”: faptele și deciziile confirmate sunt stocate separat de presupuneri și experimente. Acest lucru permite AI-ului și omului să se orienteze rapid în proiect și să înțeleagă exact starea curentă.

---

## 1. Principii de bază

- **Separă faptele de ipoteze.** Tot ce este neconfirmat trăiește doar în documentul de lucru al sarcinii curente.
- **Lucrează după PDCA (Plan Do Check Act).** Mai întâi planul și experimentul, apoi verificarea, și abia după aceea — modificările în cod și fixarea în baza de cunoștințe.
- **Înregistrează tot parcursul.** Comenzile, log-urile, versiunile, timpul — sunt obligatorii pentru trasabilitate și repetabilitate.
- **Control asupra Cursor.** Verifică diff-urile, fișierele finale, rezultatele deploy-ului și actualitatea versiunii pe server.

---

## 2. Structura documentelor

```
/Project_DOC (poți adăuga acest folder în .gitignore)
   1. Project_MAP.md      (secțiuni: Architecture, Logs, Workflows, VerifiedFacts)
   2. Collector.md        (colectarea informațiilor de pe server)
   3. Config_Settings.md  (starea serverului conform datelor din Collector)
   4. Roadmap.md          (planul general/traseul sarcinilor)
   5. Task_In_Work.md     (sarcina curentă, tabla PDCA)
   6. Rules_for_AI.md     (regulile de lucru pentru AI și proces)
   7. Doc_API.md          (document unic API compus din documentația oficială, furnizat manual și compilat de Cursor)
   8. Experiment_API.md   (practica și rezultatele experimentelor cu API)
   9. Notepad.md           (comenzi operative: git/deploy, URL-uri de test, date carduri de test)
  10. AI_Coding_Manual.md (documentul curent - memorandum privind structura fișierelor pentru interacțiunea cu AI și regulile de gestionare a proiectului și documentației)
```

---

### 2.1 `Project_MAP` — baza de cunoștințe (doar fapte)

Principala „enciclopedie” a proiectului. Conține exclusiv date confirmate:

- descrierea generală și obiectivele proiectului;
- arhitectura și interacțiunea componentelor;
- procesele de lucru și scenariile;
- în ce fișiere pe server se află log-urile și cum le analizăm;
- integrările și serviciile externe de care depinde sistemul;
- mediile utilizate, infrastructura și comenzile/procesele cheie de deploy;
- structura datelor (de exemplu: Google Sheets, serviciile MAIB) și legătura lor cu serviciile;
- componentele cheie backend (funcții, cache-uri, module principale) și modul în care participă în procese;
- diferența dintre topologia serverului (repozitorii separate prod/test pentru proiectele utilizatorilor) și structura locală pe PC/GitHub;
- endpoint-uri API confirmate și scenarii de integrare reușite;
- glosar și link-uri către documente conexe, inclusiv acesta - AI_Coding_Manual.

Completarea documentului se face doar după parcurgerea completă a ciclului PDCA, când:
1) toate ipotezele sunt confirmate prin experimente reproductibile;
2) sunt colectate artefactele sursă, este formulată descrierea finală a comportamentului sistemului.

---

### 2.2 `Collector.md` — colector de informații de pe server

Lista acțiunilor verificate pentru diagnosticare:

- comenzi și scripturi care sunt lansate;
- ce anume se analizează în log-uri și metrici;
- liste de verificare pentru monitorizare și verificări rapide;
- link-uri către vizualizări sau panouri.
- la fiecare rulare fixează data, versiunea collector și un scurt rezumat pe medii (prod/test);
- descrie ce date sunt extrase de script: statusuri systemd, prezența scripturilor de deploy și alias-urilor, starea `.env`, porturile ocupate, verificări Nginx/Certbot, structura proiectului, dependențe, log-uri de rețea și API cheie;
- amintește că raportul (`SERVER_CONFIG.md`) se actualizează manual pe server și se transferă în Cursor împreună cu artefactele actuale.

Acest document ajută AI-ul și omul să știe întotdeauna cum să obțină starea actuală a sistemului.

---

### 2.3 `Config_Settings.md` — rapoarte de la Collector, Cursor va ști ce este pe partea de server și va avea acces la informații, adică va fi la curent cu „hardware-ul”

Fixează o „secțiune” a sistemului fără interpretări:

- configurațiile curente ale serviciilor;
- starea după deploy;
- extrase din log-uri și metrici;
- versiuni, hash-uri, marcaje temporale;
- orice rezultate faptice ale verificărilor.
- rezumate tabelare pentru mediile prod/test (porturi, căi, servicii, comenzi deploy);
- status systemd, prezența scripturilor de deploy/alias-urilor și rezultatele rulării lor;
- starea `.env`, versiunile Python și porturile active, verificări Nginx/Certbot, utilizarea resurselor;
- răspunsurile actuale `/version` și OpenAPI, lista log-urilor, structura proiectului, dependențe, variabile de mediu.

Important: nicio concluzie, doar date „așa cum sunt”.

---

### 2.4 `Roadmap.md` — planul general al proiectului

Scheletul dezvoltării proiectului:

- etape mari (Epic);
- sarcini de nivel Task;
- subsarcini și pași de execuție;
- dependențe și secvența de execuție.

La descoperirea unei complexități — divizăm sarcina direct aici, pentru ca planul să rămână actual și realist.

---

### 2.5 `Task_In_Work.md` — tabla de lucru (Whiteboard)

Singurul document unde se desfășoară munca curentă. Structura reflectă ciclul PDCA.

1. **Formularea sarcinii.** Clar, cu criteriu de succes.
2. **Diagnosticare (Plan).** Observații, simptome, ipoteze, întrebări.
3. **Planul experimentelor.** Pași cu rezultate așteptate și criterii de verificare, cum diagnosticăm..., cum verificăm...
4. **Experimente (Do).** Acțiuni secvențiale Cursor/om cu fixarea comenzilor, log-urilor și iterațiilor intermediare.
5. **Fapte (Check).** Doar succese confirmate: ce a funcționat, ce comenzi, unde se află log-urile, marcaje temporale, versiuni.
6. **Concluzii și soluții (Act).** Înțelegerea finală, soluția problemei; doar în această etapă, după înțelegerea confirmată, modificăm codul și lansăm deploy-ul.
7. **Finalizare.** După deploy rulăm teste de control; dacă sarcina din `Roadmap` este închisă și rezultatul confirmat, transferăm faptele și concluziile finale în `Project_MAP`, actualizăm `Roadmap`, curățăm `Task_In_Work` pentru următoarea sarcină. Sarcinile finalizate le marcăm ca „Gata” și le lăsăm în listă pentru trasabilitate.

---

### 2.6 `Rules_for_AI.md` — regulament pentru AI

Instrucțiune pentru ca Cursor să lucreze fiabil.

**Reguli generale:**
- nu trece la modificarea codului până când în `Task_In_Work` nu sunt parcurse etapele Check și Act (există fapte confirmate, sunt formulate concluzii și soluția);
- orice experiment se documentează: pas, rezultat, legătură cu timpul;
- faptele de succes — în `Project_MAP`, ciornele și ipotezele — doar în `Task_In_Work`.

**Înainte de modificarea codului:**
- arată modificările presupuse (diff);
- clarifică influența asupra celorlalte părți ale sistemului;
- analizează funcționalitatea afectată pentru conflicte și efecte secundare (pentru ca repararea unui nod să nu strice altele);

**După modificare:**
- afișează fișierele actualizate;
- verifică actualitatea versiunii pe server;
- pregătește comentariul pentru commit;
- inițiază colectarea log-urilor/metricilor prin `Collector`, dacă este necesar și imaginea se completează cu noi „piese de puzzle”.

**Verificarea acțiunilor Cursor:**
- compararea diff-ului și a fișierului final;
- controlul deploy-ului și starea serviciilor;
- confirmarea versiunii/hash-ului pe server.

**Comenzi rapide pentru AI:**
- „Efectuează diagnosticarea și verificarea ipotezei N din `Task_In_Work` prin curl direct pe server; arată comenzile și afișează rezultatele”.
- „Reverifică și completează `Collector` pentru serviciul X și eu voi actualiza `Config_Settings` cu artefacte proaspete”.
- „Adună faptele confirmate din ultimul experiment și rezumă-le într-o intrare pentru `Project_MAP`”.

---

### 2.7 `Doc_API.md` — fițuică pentru documentație

Conspect după studierea materialelor oficiale (manual cu ajutorul Cursor, Perplexity doar pentru verificare):

- endpoint-uri cheie și scopul lor;
- parametri și limitări;
- cereri/răspunsuri tipice;
- indicii privind autentificarea, limitele, erorile;
- schema de generare și actualizare access token (generate-token, refreshToken) și regulile de viață ale acestuia;
- cerințe pentru parametri, de exemplu `pay` (câmpuri obligatorii, `callbackUrl`, `okUrl`, `failUrl`);
- formatul notificărilor callback, structura de exemplu (`result`), statusuri și politica retrimiterilor;
- schema de bază a validării semnăturii (ce câmpuri participă, unde se stochează SignatureKey);
- principiul utilizării aceluiași endpoint pentru test și production (diferențe doar în credențialele proiectului);
- link-uri către sursele originale.

Cu alte cuvinte, aceasta este baza de cunoștințe despre API-ul integrărilor proiectului meu cu alte servicii.

**Cum să faci manual cu ajutorul Cursor `Doc_API_MAIB.md`:**
Creează un document gol Doc_API.md cu structura de bază a documentației API.
Apoi voi trimite informații în blocuri.
De fiecare dată când trimit un nou bloc de informații:
-  inserează-l în secțiunea corespunzătoare a documentului,
-  nu schimba sensul,
-  nu omite nimic,
-  nu reformula detaliile tehnice,
-  nu duplica informația, dacă ea este deja prezentă în document.
-  La necesitate poți extinde structura documentului, dacă blocul de informații necesită logic o nouă secțiune.
-  Poți adăuga comentarii în limba rusă (sau română, în funcție de context), pentru a explica structura, alegerea secțiunilor și logica integrării.
În final documentul trebuie să iasă ca un conspect-bază de cunoștințe după studierea materialelor oficiale privind integrările API ale proiectului meu cu diverse servicii externe.

**Cum să dai o sarcină Perplexity sau altui AI pentru verificarea `Doc_API_MAIB.md`:**

- **Sarcină (TASK)**:
  „Verifică acest document `Doc_API_MAIB.md` — o fițuică scurtă și structurată despre MAIB e-Commerce API”, dacă nu am omis nimic, și cum se poate structura mai bine acest document, pentru a fi mai practic pentru AI și mai corect tehnic.

---

### 2.8 `Experiment_API.md` — practică și scenarii verificate

Catalog viu al experimentelor faptice cu API extern:

- cereri reale de lucru cu parametri;
- răspunsuri reușite și interpretarea datelor;
- particularități de comportament, nedescrise în documentație;
- neconformități și bug-uri găsite;
- link-uri către log-uri și versiuni confirmate;
- obiective scurte ale experimentului și status (în lucru/succes/eșec);
- pas cu pas: comenzi utilizate (de exemplu, curl) și fapte fixate pentru fiecare pas;
- parametri obligatorii găsiți și cauzele reale ale problemelor (ca în cazul cu 404 și încărcarea incorectă a `.env`).

La apariția unui nou fapt verificat:
1. Îl fixăm aici.
2. La necesitate actualizăm `Doc_API`.
3. Dacă este critic pentru proiect — transferăm în `Project_MAP`.

---

### 2.9 `Notepad` — fițuică rapidă

- scenariu tipic de publicare: `git status → git add . → git commit → git push → deploy-*`;
- comenzi scurte de referință și căi pentru mediul de test și prod;
- date de card de test MAIB pentru plăți recurente.

---

## 3. Ciclul de lucru (PDCA în acțiune)

1. **Plan.** Luăm sarcina din `Roadmap`, o transferăm în `Task_In_Work`, formăm ipoteze și planul experimentelor.
2. **Do.** Pas cu pas executăm experimentele, prin curl și analiza log-urilor, fixând rezultatele în `Task_In_Work`.
3. **Check.** Selectăm faptele confirmate, le transferăm în secțiunile corespunzătoare din `Task_In_Work` (sau în unele cazuri în `Experiment_API` sau `Config_Settings`).
4. **Act.** Pe baza faptelor introducem modificări în cod, facem deploy, verificăm starea, completăm `Project_MAP`, actualizăm `Roadmap`, marcăm sarcina ca finalizată dacă testul final după modificarea codului a fost reușit, și luăm următoarea sarcină în lucru.

După finalizarea ciclului documentul de lucru `Task_In_Work` se curăță, și procesul se repetă pentru următoarea sarcină/subsarcină.

---

## 4. Controlul versiunilor și deploy

- După deploy verifică neapărat că serverul conține codul actualizat (compararea versiunilor, configurațiilor, log-urilor).
- În cazul desincronizării documentează imediat problema și pașii întreprinși.

---

## 5. Rolul AI în proces

- AI ajută la colectarea faptelor, formatarea documentelor și generarea ideilor, dar nu ia decizii fără confirmări.
- Orice acțiune AI trebuie să fie documentată transparent și verificată de om.
- AI scrie cod, și o face mult mai bine și mai optimizat decât omul.

---

## 6. Start rapid Project_MAP

1. Creează structura de fișiere și foldere descrisă.
2. Completează `Project_MAP` și `Roadmap.md` cu cunoștințele curente.
3. Transferă sarcina activă în `Task_In_Work.md` și lansează ciclul PDCA.
4. Completează regulat documentele cu fapte și curăță masa de lucru după finalizarea sarcinilor.

Această schemă permite gestionarea sistemică a proiectului, ordonarea memoriei colective și utilizarea eficientă a Cursor ca asistent.

