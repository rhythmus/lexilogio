Deze regels bieden een rigide kader voor het consistent onderhouden en uitbreiden van de woordenschatlijst.

## Algemene Bestandsformaat Regels

1.  **Tekstcodering (Encoding):** Het bestand dient UTF-8 codering te gebruiken om Griekse karakters, diakritische tekens en andere speciale symbolen correct weer te geven.
2.  **Scheidingsteken (Delimiter):** Velden binnen elk record (regel) worden gescheiden door een puntkomma (`;`).
3.  **Lege Velden:** Indien een veld geen waarde heeft, dient het nog steeds afgebakend te worden met puntkomma's (bijv. `;;` voor een leeg veld tussen twee andere velden, of een puntkomma aan het einde van een regel indien het laatste veld leeg is). Elk record dient idealiter 6 puntkomma's te bevatten (voor 7 velden).
4.  **Koptekstregel (Header Row):** De eerste regel van het bestand is een koptekstregel die de kolomnamen definieert:
    ```csv
    nr;datum;Nederlands;Grieks;woordsoort;nota;thema
    ```
5.  **Recordstructuur:** Elke regel na de koptekstregel vertegenwoordigt één woordenschatitem.

## Kolomspecifieke Regels en Syntaxisconventies

### 1. `nr` (Volgnummer/Identificatie)

**Doel:** Een unieke identificatiecode voor het woordenschatitem.

**Beperking:** Verplicht. Moet uniek zijn voor elk item.

1.1 **Syntaxis:** viercijferig nummer, vaak voorafgegaan door nullen (bijv. `0002`, `0158`).

### 2. `datum` (Datum)

**Doel:** Geeft een datum aan die geassocieerd is met het item, mogelijk wanneer het is toegevoegd, herhaald (in de les) of relevant is.

2.1 **Syntaxis:** Datums zijn in `MM-DD` formaat (bijv. `04-22`, `03-11`).
2.2 Meerdere datums voor een enkel item worden gescheiden door een komma gevolgd door een spatie (bijv. `03-11, 05-06`).
2.3 **Beperking:** Optioneel.

### 3. `Nederlands` (Nederlandse Vertaling)

**Doel:** Het Nederlandse woord, de frase of zin.

**Beperking:** Verplicht.

3.1 **Syntaxis:** Platte tekst.
3.2 **Kapitalisatie:**
  - Zinnen, vragen, uitdrukkingen: Beginhoofdletter en correcte zininterpunctie (. ! ? …).
  - Eigennamen/plaatsnamen: Beginhoofdletter.
  - Alle andere items (losse woorden, korte frasen): kleine letter.
3.3 **Deductie/Vereenvoudiging:**
  - Verwijder onnodige lidwoorden en meervouden tenzij contextueel vereist.
  - Behoud enkel de kerngedachte van de vertaling; extra informatie verhuist naar de `nota` kolom.
  - Alternatieve Nederlandse vertalingen of formuleringen voor hetzelfde item worden gescheiden door een spatie, een pipe-symbool en nog een spatie (` | `) (bijv. `Welkom! | Gij zijt welkom.`).
3.4 Haakjes `()` worden gebruikt om aan te duiden:
  - Optionele delen van een woord of frase (bijv. `Hoe gaat het (met je)?`).
 - Korte verduidelijkingen of context die direct verband houden met de Nederlandse term (bijv. `mountza (beledigend handgebaar)`).
 

### 4. `Grieks` (Griekse Vertaling)

**Doel:** Het Griekse woord, de frase of zin.

**Beperking:** Verplicht.
   
*   **Syntaxis:**
    *   Tekst in Grieks schrift, inclusief alle noodzakelijke accenttekens (tonos).
    *   **Kapitalisatie:**
        *   Zinnen, vragen, uitdrukkingen: Beginhoofdletter en correcte zininterpunctie (. ! ; …).
        *   Eigennamen/plaatsnamen: Beginhoofdletter.
        *   Alle andere items (losse woorden, korte frasen): kleine letter.
    *   **Zelfstandige naamwoorden (Artikelen):**
        *   Eigennamen, abstracte zelfstandige naamwoorden en filosofische concepten die in het Grieks standaard het bepaald lidwoord vereisen, krijgen dit lidwoord ervoor zonder haakjes (bijv. `ο Αχιλλέας`, `η φιλοσοφία`).
        *   Andere zelfstandige naamwoorden krijgen het lidwoord doorgaans tussen haakjes ervoor (bijv. `(ο) καφές`).
        *   Zelfstandige naamwoorden die zowel mannelijk als vrouwelijk kunnen zijn, krijgen `(ο/η) ` (of `ο/η ` indien het altijd zonder haakjes is, dit punt dient nog verduidelijkt te worden op basis van consistente toepassing).
        *   Na de enkelvoudsvorm *moet*, indien van toepassing, de meervoudsvorm gegeven worden, gescheiden door ` - `, vaak ook met het lidwoord tussen haakjes (bijv. `(η) γυναίκα - (οι) γυναίκες`, `(το) παιδί - (τα) παιδιά`).
    *   **Synoniemen:** Synoniemen worden alfabetisch gesorteerd en gescheiden door een komma en een spatie (bijv. `άσπρος -η -ο, λευκός -ή -ό`). (Dit wijkt af van de ` | ` separator die in `lexilogio.csv` soms wordt gebruikt; conform `rules.md` is dit de aanpassing).
    *   Haakjes `()` worden verder gebruikt om aan te duiden:
        *   Grammaticale informatie zoals geslacht/getal markeringen (bijv. `-η -ο` voor bijvoeglijke naamwoorden, `(ev.)` voor enkelvoud, `(mv.)` voor meervoud).
        *   Optionele delen van een woord/frase.
        *   Korte fonetische transcripties, meestal tussen schuine strepen (bijv. `/pjos íesè/`), hoewel dit zeldzaam is en ook in de `nota` kolom kan voorkomen.
    *   Volledige werkwoordsvervoegingen of meerdere vormen kunnen direct worden vermeld als zij het primaire item vormen (bijv. `ταξιδεύω - ταξιδεύεις ...`).
    *   **Voorzetsels:** Indien relevant, wordt de vereiste naamval gespecificeerd (bijv. `από + acc.`).


### 5. `woordsoort` (Woordtype/Deel van Spraak)

**Doel:** Specificeert de grammaticale categorie van het item.
   
**Beperking:** Over het algemeen verplicht. Dient een enkele herkende afkorting of term te zijn.

*   **Syntaxis:** Gebruikt gestandaardiseerde Nederlandse afkortingen. Veelvoorkomende afkortingen zijn:
    *   `znw.` (zelfstandig naamwoord)
    *   `uitdr.` (uitdrukking)
    *   `ww.` (werkwoord)
    *   `bnw.` (bijvoeglijk naamwoord)
    *   `bw.` (bijwoord)
    *   `vz.` (voorzetsel)
    *   `vnw.` (voornaamwoord)
    *   `telw.` (telwoord)
    *   `voegw.` (voegwoord)
    *   `zin` (zin/frase)
    *   `eigennaam` (eigennaam)
    *   `plaatsnaam` (plaatsnaam)
    *   `morfeem` (morfeem)
    *   `znw. groep` (zelfstandig naamwoord groep)
    *   `ww. groep` (werkwoord groep)
    *   `vraagzin` (vraagzin/interrogatieve zin) - dit verschijnt vaak in het `nota` veld, maar soms hier.
    *   Indien de bron een complexere of niet-standaard woordsoort heeft, wordt deze toegewezen aan de meest overeenkomstige Nederlandse afkorting.


### 6. `nota` (Notitie)

*   **Doel:** Biedt extra context, uitleg, grammaticale details, etymologie, gebruiksinformatie of culturele informatie.
*   **Syntaxis:**
    *   Vrije tekst.
    *   Kan bevatten:
        *   Referenties of vergelijkingen (bijv. `cfr Fr. ‘voici’`).
        *   Formaliteitsniveau (bijv. `formeel`, `informeel`).
        *   Gebruiksvoorwaarden (bijv. `wanneer iemand niest`, `gebruiksnotities`).
        *   Specifieke grammaticale details die niet onder `woordsoort` vallen (bijv. `2e ev.`, `diminutief`, `meervoud`, `ww. suffix`, `vocatief`, `passief`).
        *   Etymologische informatie (bijv. `etym. ‘Is-tan-bul’`).
        *   Korte uitleg over betekenis of gebruik (bijv. `witte harswijn`, `typisch Grieks concept`).
        *   Uitspraakgidsen (bijv. `/i Mérri/`), hoewel deze ook in het Griekse veld kunnen voorkomen.
        *   Letterlijke vertalingen of uitleg van idiomen (bijv. `lett. ‘Hoe noemen ze je?’`).
    *   Enkele aanhalingstekens (`' '`) of standaard dubbele aanhalingstekens (`" "`) kunnen worden gebruikt voor nadruk of om letterlijke strings/voorbeelden aan te duiden.
*   **Beperking:** Optioneel.

### 7. `thema` (Thema/Onderwerp)

*   **Doel:** Categoriseert het woordenschatitem op onderwerp of thema.
*   **Syntaxis:**
    *   Eén of meerdere trefwoorden.
    *   Meerdere thema's voor een enkel item worden gescheiden door een komma gevolgd door een spatie (bijv. `grammatica, reizen`, `kennismaken, geografie, wonen`).
    *   Het ampersand-teken (`&`) wordt gebruikt binnen themanamen (bijv. `groeten & wensen`).
    *   Veelvoorkomende thema's (gebaseerd op `lexilogio.csv`, idealiter afgestemd op een masterlijst): `groeten & wensen`, `taalkunde`, `namen`, `filosofie`, `voedsel`, `beroepen`, `geografie`, `relaties`, `hoeveelheden`, `activiteiten`, `kleuren & vormen`, `dingen`, `kalender`, `emoties`, `natuur`, `muziek`, `gebouwen`, `reizen`, `kleding`, `maatschappij`, `wonen`, `media`, `lichaam`, `winkelen`, `grammatica`, `cultuur`, `uitdrukkingen`, `gebeurtenissen`.
    *   Het thema wordt afgeleid van de betekenis en context van het woord, overeenkomstig een vastgestelde lijst of zoals bepaald in eerdere batches.
*   **Beperking:** Optioneel, maar sterk aanbevolen voor organisatie.

## Algemene Regels (Toepasbaar op Alle Kolommen)

*   **Kapitalisatie en Interpunctie Synchronisatie:** Kapitalisatie en interpunctie worden enkel gesynchroniseerd tussen de Nederlandse en Griekse kolom voor volledige zinnen, vragen, uitdrukkingen en eigennamen/plaatsnamen. Voor losse woorden/korte frasen geldt de specifieke kapitalisatieregel per taal (zie `Nederlands` en `Grieks` secties).
*   **Deductie en Vereenvoudiging (Nederlands):** Onnodige lidwoorden en meervouden worden in de Nederlandse kolom verwijderd, tenzij contextueel vereist. De kerngedachte van de vertaling wordt behouden.
*   **Verplaatsing Extra Info:** Overige informatie die niet direct tot de kernvertaling behoort, wordt verplaatst naar de `nota` kolom.
*   **Standaardisatie `woordsoort` en `thema`:** De waarden in de `woordsoort` en `thema` kolommen worden gestandaardiseerd en consistent toegepast volgens de gedefinieerde afkortingen en themalijsten.
