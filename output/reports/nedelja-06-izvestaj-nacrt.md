# Nedeljni izveštaj — NACRT

## 1. Osnovne informacije

| Polje | Odgovor |
| --- | --- |
| Ime i prezime | Isidora Popović |
| Adresa e-pošte | popovicisidora17@gmail.com |
| Discord korisničko ime | Nije navedeno |
| Nedelja | 6 — Retrieval Augmented Generation (RAG) |
| Par / tim | Isidora Popović i Elena |
| Moj konkretan doprinos / uloga | Rad na kodu i pregled izmena; Elena je pregledala kod i izveštaj i dopunila ono što je trebalo doraditi, nakon čega sam pregledala dopune. |
| Datum predaje | 2026-10-12 |
| Reference na rad i dokaze | `evidence.md`, dokumentovani primeri za zadatke 01–05, transkript `checklist-validation.txt` i commitovi `bee26a7`, `08922ef`, `82c50da`, `5d75029`, `d0432a3` i `2c03041`. |

Demo lead nije naveden.

## 2. Moj status

**Status:** Delimično završeno

Tehnički deo svih pet zadataka je završen i dokumentovan, uključujući opciono poboljšanje leksičkog bodovanja. U poslednjoj proveri svih 34 testa su prošla. Za potpunu predaju preostaju podaci o demo lead-u i dopuna ličnih podataka u izveštaju.

## 3. Rad ove nedelje

Ove nedelje radila sam na Week 6 RAG zadatku. Cilj je bio da uporedimo uticaj chunkinga na pronalaženje relevantnog konteksta, proverimo top-k retrieval, obezbedimo odgovore sa citatima i odbijanje pitanja za koja korpus nema dovoljno dokaza. Za svaki zadatak napravljena je posebna Markdown dokumentacija, a zatim su rezultati objedinjeni u `evidence.md`.

Moj deo rada bio je rad na kodu i pregled izmena. Elena je pregledala kod i izveštaj i dopunila delove koje je trebalo doraditi. Pregledala sam i te dopune. Svi dokumenti su provereni, kod je pročitan i nije bilo automatskog odobravanja izmena. Pitala sam i da li rešenje može da se optimizuje i poboljša.

U prvom zadatku poređene su konfiguracije `chunk_size=140, overlap=30` i `chunk_size=80, overlap=20`, za isto pitanje i isti korpus. Manji chunkovi su imali viši leksički rezultat, ali su delili važnu rečenicu i počinjali usred reči. Zadržane su podrazumevane vrednosti 140/30 jer je prvi rezultat čuvao celu rečenicu relevantnu za pitanje. Ova odluka važi za testirani primer, a ne kao univerzalno najbolja konfiguracija.

Zatim je provereno da top-k retrieval vraća rezultate u opadajućem redosledu bodova, uz primere za k=2 i k=3. Provereni su i jednaki bodovi, prag filtriranja i slučajevi kada ima manje relevantnih rezultata nego što je traženo. Dokumentovano je da ispravno numeričko rangiranje ne garantuje smislen odgovor: zajedničke reči poput „and” mogu da podignu nerelevantan tekst.

Za citate je upotrebljeno pitanje „Why are citations important in RAG?”. Provereno je da identifikator u odgovoru odgovara stvarno pronađenom chunku i da je citirani tekst identičan izvornom tekstu. Za ovaj primer korišćeni su chunk size 220, overlap 30 i top-k 1, kako bi cela rečenica o transparentnosti, poverenju i proveri dokaza ostala sačuvana. Podrazumevane vrednosti aplikacije nisu promenjene.

Važan neuspešan slučaj bio je pitanje „Who won the world cup in 1958?”. Sistem ga je prvobitno prihvatao i vraćao nepovezane RAG odlomke zbog poklapanja zajedničkih reči. Dodat je uslov da pronađeni kontekst mora da deli bar jednu sadržajnu reč sa pitanjem. Posle izmene, ovo pitanje i pitanje „Zanzibar population 2025?” vraćaju jasnu poruku odbijanja bez citata. Ovo je leksička zaštita; samo poklapanje sadržajne reči još ne dokazuje da odlomak zaista podržava odgovor.

Koristila sam Codex za pripremu zadataka, implementaciju izmena, testove, dokumentovanje dokaza i Git commitove. U ovoj sesiji Codex je izvršavao testove i CLI provere. Moja provera obuhvatila je čitanje koda i dokumenata i razmatranje mogućih poboljšanja; te aktivnosti razlikujem od automatski izvršenih provera. Dodatno je uvedena opcija `--ignore-common-words`, koja poboljšava leksičko bodovanje, uz šest testova za proširenje. Proverena je i instalacija u novom izolovanom okruženju sa tačno propisanim `pytest==8.3.3`. Poslednja zabeležena provera dala je `34 passed in 0.07s`, a podržani i nepodržani završni primer prošli su proveru.

Rad sa RAG-om mi je već bio poznat, ali sam kroz ovaj zadatak učvrstila znanje. Nastaviću da ga primenjujem na ličnim projektima. Ograničenja rešenja ostaju deljenje reči pri chunkingu, mogući slabi leksički rezultati i činjenica da aplikacija kopira pronađeni kontekst umesto da generiše novi sažeti odgovor.

Potreba za dodatnom pomoći tutora nije navedena.

## 4. Sledeći korak

Nastaviću da primenjujem RAG na ličnim projektima. Konkretna sledeća aktivnost i kriterijum završetka još nisu navedeni.

## 5. Poverljiva napomena za tutora

Nema dodatne napomene.
