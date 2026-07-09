# Eventi a Prato

## Sistema di gestione eventi

*Autore*: Simone Ferri  
*Tipo di progetto*: Full-Stack Web Application  
*Framework utilizzato*: Django 

---

## Indice
1. [Descrizione dell’applicazione](#descrizione-dellapplicazione)
   - [Tipologie di utenti](#tipologie-di-utenti)
2. [Funzionalità implementate nell’applicativo](#funzionalità-implementate-nellapplicativo)
   - [Funzionalità dell’admin](#funzionalità-delladmin)
   - [Funzionalità del redattore](#funzionalità-del-redattore)
   - [Funzionalità del fruitore](#funzionalità-del-fruitore)
3. [Elenco delle pagine del sito](#elenco-delle-pagine-del-sito)
4. [Requisiti condizionali](#requisiti-condizionali)
5. [Organizzazione del codice del progetto Django](#organizzazione-del-codice-del-progetto-django)
6. [Specifiche per i test sull’applicativo](#specifiche-per-i-test-sullapplicativo)
   - [Istruzioni per l'installazione in locale](#istruzioni-per-installazione-in-locale) 
   - [Database](#database)
   - [Demo account](#demo-account)
   - [Link di deployment](#link-di-deployment)
7. [Scenari di test](#scenari-di-test)

---

## Descrizione dell’applicazione

L’applicativo simula un sito per l’inserimento, la consultazione e la prenotazione di eventi di varie tipologie. 

### Tipologie di utenti

Sono previste tre tipologie di utenti:

* **amministratore** del sito, che gestisce tutto dall’interfaccia di amministrazione di default di Django. Ha i permessi per fare tutto ma il suo compito principale è l’abilitazione dei redattori
* **redattore**: può gestire gli eventi, le tipologie di evento e le prenotazioni ai suoi eventi. I redattori appartengono al gruppo “redattori”
* **fruitore**: può consultare gli eventi, prenotare un evento e cancellare una prenotazione. Gli utenti autenticati appartengono di default al gruppo “visitatori”

In aggiunta alle tipologie precedenti abbiamo anche il visitatore anonimo che può solo consultare gli eventi.

---

## Funzionalità implementate nell’applicativo

### Funzionalità dell’admin

Nella progettazione dell’applicativo è stato deciso di assegnare alla figura dell’admin il ruolo di coordinatore del sistema. Trattandosi di un ambiente redazionale distribuito è necessaria la presenza di un amministratore che decida chi può inserire gli eventi e che faccia da mediatore quando sono necessarie scelte che richiedono la condivisione di tutti (es: l’eliminazione di una tipologia). 

La sua funzione principale è quella di abilitare i redattori inserendo il loro utente (dopo che si sono iscritti al sistema) nel gruppo “redattori”, è anche l’unico che può eliminare una tipologia di evento.

### Funzionalità del redattore

I redattori si iscrivono al sistema come tutti gli utenti, è compito dell’admin assegnare loro il gruppo “redattori” in modo che possano gestire gli eventi.

Il ruolo del redattore è totalmente distinto da quello di fruitore, un redattore che vuole agire sulla piattaforma come fruitore deve registrarsi e accedere con un profilo diverso.

Un redattore può inserire, modificare, annullare e cancellare un evento (la cancellazione è soggetta a condizioni specifiche). Le operazioni di modifica/annullamento/cancellazione sono possibili sono negli eventi inseriti dal redattore stesso e non su quelli inseriti dagli altri redattori.

Un redattore può inserire o modificare una tipologia. Le operazioni di modifica sono possibili solo nelle tipologie inserite dal redattore stesso e non su quelle inserite dagli altri redattori. Un redattore non può eliminare una tipologia.

Un redattore può consultare una sezione (Gestione eventi) in cui sono presenti tutti gli eventi che ha inserito, sia quelli futuri che quelli già passati, distinti in due elenchi diversi.

Da una qualunque pagina in cui è presente un elenco di eventi, cliccando sul nome dell’evento si arriva nella pagina di dettaglio dalla quale è possibile modificare o eliminare un evento se l'evento è stato inserito del redattore stesso. Un redattore può anche prenotare un evento ma deve prima autenticarsi con un profilo di fruitore.

Se nell’evento sono presenti prenotazioni è possibile cliccare su un link (“dettaglio prenotazioni”) che porta ad una pagina con l’elenco di tutte le prenotazioni presenti per quell’evento. Il redattore può cancellare una prenotazione ma solo in casi eccezionali (apertura di una finestra di avviso).

I redattori possono modificare i loro dati dalla sezione “Modifica utente” e cambiare la password dalla sezione “Cambia password”.

### Funzionalità del fruitore

Gli utenti si iscrivono al sistema utilizzando la maschera di SignUp e viene loro assegnato in automatico il gruppo “visitatori” che gli assegna i permessi necessari per poter prenotare gli eventi e gestire le proprie prenotazioni.

I fruitori possono consultare gli eventi pubblicati e fare una prenotazione per uno o più eventi. Ogni fruitore può fare solo una prenotazione.

Se sono presenti delle prenotazioni queste vengono mostrate al fruitore (autenticato sul sito) sia sulla home page che nell’apposita sezione “Eventi prenotati” in cui sono presenti tutti gli eventi che ha prenotato, sia quelli futuri che quelli già passati, distinti in due elenchi diversi.

I fruitori possono inserire o cancellare le loro prenotazioni dalla pagina di dettaglio di ogni evento.

I fruitori possono modificare i loro dati dalla sezione “Modifica utente” e cambiare la password dalla sezione “Cambia password”.

---

## Elenco delle pagine del sito

Nel sito gli utenti possono accedere alla seguenti pagine:

* **Home** (accessibile a tutti), in questa pagina sono presenti:
  * menu principale con:
    * link alla home (visibile a tutti)
    * link alla pagina “Tutti gli eventi” (visibile a tutti)
    * link alla pagina “Eventi prenotati” (visibile solo ai fruitori con almeno una prenotazione)
    * bottone per fare il login (visibile a tutti)
    * bottone per fare iscriversi (visibile a tutti)
    * menu utente (visibile solo agli autenticati)
    
    *Nota*: il menu principale è uguale in tutte le pagine per cui la descrizione non viene ripetuta nei punti successivi
  * un avviso sulla presenza di eventi annullati per i quali il fruitore aveva fatto una prenotazione (visibile solo ai fruitori solo se si verifica il caso)
  * una sezione con i prossimi 4 eventi prenotati (visibile solo ai fruitori che hanno almeno 1 evento prenotato)
  * una sezione con i prossimi 6 eventi in programma (visibile a tutti)

* **Tutti gli eventi** (accessibile a tutti), in questa pagina sono presenti:
  * filtri per tipologia che permetta di visualizzare solo gli eventi della tipologia selezionata (visibile a tutti)
  * Elenco di tutti gli eventi futuri con paginazione (visibile a tutti)

* **Eventi prenotati** (accessibile solo ai fruitori), in questa pagina sono presenti:
  * un avviso sulla presenza di eventi annullati per i quali il fruitore aveva fatto una prenotazione (se si verifica il caso)
  * un elenco degli eventi futuri prenotati dall’utente
  * un elenco degli eventi passati prenotati dall’utente

* **Gestione eventi** (accessibile solo ai redattori dal menu utente), in questa pagina sono presenti:
  * i bottoni per inserire un nuovo evento o una nuova tipologia
  * un elenco degli eventi futuri inseriti dal redattore
  * un elenco degli eventi passati inseriti dal redattore

* **Scheda singolo evento** (accessibile a tutti), in questa pagina sono presenti:
  * Informazioni relative al singolo evento (titolo, descrizione, data, ecc..) compreso lo stato annullato
  * Le prenotazioni effettuate e quelle disponibili
  * Il bottone per prenotarsi (solo per fruitori che non si sono già prenotati)
  * Info sulla presenza di una prenotazione e il bottone per cancellare la prenotazione (solo per fruitori che si sono già prenotati)
  * Il bottone per modificare l’evento (solo per il redattore dell’evento)
  * Il bottone per eliminare l’evento (solo per il redattore se non ci sono prenotazioni attive)
  * Il bottone per loggarsi e prenotare l’evento (per tutti gli utenti anonimi ed i redattori)

* **Prenotazioni per l'evento [nome evento]** (accessibile solo al redattore dell’evento), in questa pagina viene mostrato un elenco di tutte le prenotazioni attive per l’evento selezionato.

* **Maschera di inserimento/modifica dell’evento** (accessibile solo ai redattori). La maschera di inserimento è accessibile con un bottone presente nel menu utente o in cima alla pagina di gestione degli eventi.

* **Maschera di inserimento/modifica della tipologia** (accessibile solo ai redattori). La maschera di inserimento è accessibile con un bottone presente nel menu utente o in cima alla pagina di gestione degli eventi. In questa pagina sono presenti:
  * la maschera di inserimento/modifica
  * un elenco con tutte le tipologie già inserite. Accanto ad ogni tipologia viene visualizzato il nome del redattore che l’ha inserita o il bottone di modifica se è stata inserita dal redattore che sta consultando la pagina

* **Maschera di modifica dati utente** (accessibile solo agli utenti autenticati)

* **Maschera di modifica password** (accessibile solo agli utenti autenticati)

---

## Requisiti condizionali

Ci sono tutta una serie di precondizioni e di requisiti che sono stati scelti nella progettazione e realizzazione dell’applicativo e che vengono qui brevemente elencati:

* ogni fruitore può fare solo una prenotazione per ogni evento
* un evento può avere più di una tipologia. È stato deciso di non mettere un limite fisso ma in un caso reale ai redattori sarebbe suggerito di non usarne più di tre
* un redattore non può eliminare una tipologia ma solo modificare il nome
* se terminano i posti prenotabili sparisce il bottone di prenotazione dall’evento
* un evento può essere inserito con 0 posti prenotabili, in quel caso un messaggio avvisa che non è richiesta la prenotazione
* se sono presenti prenotazioni su un evento il redattore non può eliminarlo o spubblicarlo
* un evento annullato non può essere prenotato
* gli eventi passati spariscono dall’elenco degli eventi, restano solo nell’elenco degli eventi inseriti da un redattore. Sono anche visibili se richiamati direttamente con la url ma mostrano un messaggio di avviso sul fatto che l’evento è passato
* gli eventi spubblicati spariscono dall’elenco degli eventi, restano solo nell’elenco degli eventi inseriti da un redattore con la dicitura “spubblicato”
* gli eventi annullati non spariscono dall’elenco degli eventi ma appare la dicitura “annullato”
* solo l’admin può inserire un utente nel gruppo dei redattori
* tutti gli utenti che si iscrivono di default sono assegnati al gruppo “visitatori”



---

## Organizzazione del codice del progetto Django

La cartella principale del progetto è la cartella **“sistemagestioneeventi”**, il progetto poi è stato organizzato in quattro app distinte:

* **eventi_gestione**: qui è definito tutto ciò che riguarda gli oggeti “evento” e “tipologia”, in particolare i modelli, le viste ed i form per le operazioni CRUD
* **eventi_accounts**: qui è definito tutto che riguarda gli utenti, in particolare il modello dell’utente personalizzato, le view per l’iscrizione e la modifica dell’utente, la form per l’iscrizione
* **eventi_prenotazione**: qui è definito tutto ciò che riguarda le prenotazioni, in particolare il modello e le view per l’inserimento e la cancellazione
* **eventi_pagine**: qui è definito tutto ciò che riguarda le pagine di navigazione, in particolare le viste per la home, per l’elenco di tutti gli eventi, per l’elenco degli eventi prenotati dall’utente, per il dettaglio evento, per l’elenco degli eventi inseriti dal redattore, per l’elenco delle prenotazioni

I template sono stati definiti tutti in un’unica cartella **templates**.

Le immagini degli eventi sono salvate tutte nella cartella **media**.

Css e immagini utilizzati per il layout sono sotto la cartella **static**.

---

## Specifiche per i test sull’applicativo

In questa sezione sono fornite le specifiche utili per la fase di test del funzionamento dell’applicativo realizzato.

### Istruzioni per installazione in locale

Per l’installazione in locale dell’applicativo si possono seguire i seguenti passi:

1. Clonare il repository sulla macchina locale. Aprire il terminale e digitare:

   *git clone [https://github.com/simoneferri-repo/SistemaGestioneEventi.git](https://github.com/simoneferri-repo/SistemaGestioneEventi.git)*

   e per entrare nella cartella del progetto:

   *cd SistemaGestioneEventi*

   Si assume che sul PC siano già installati Python e Git.

2. Creare l'ambiente virtuale. Nel caso venga utilizzato Conda, dovremo digitare:

   *conda create \-n django python=3.12 \-y*

   e per attivare l’ambiente virtuale

   *conda activate django*

   Nota: *django* è il nome dell’ambiente, può essere un nome qualunque.

3. Installare le dipendenze. Le dipendenze sono tutte elencate nel file requirements.txt, quindi dovremo digitare:

   *pip install \-r requirements.txt*  
4. Configurare il database. Nel repository è già presente un database popolato (db.sqlite3) quindi non è necessario configurare il database. Se volete partire da un db vuoto eliminate il file db.sqlite3 ed eseguite il comando:

   *python manage.py migrate*

5. Configurare il superuser. Come specificato al punto precedente nel repository è già presente un database popolato in cui quindi è già definito un superuser. Anche qui, se partite da un db vuoto è necessario creare il superuser con il comando:

   *python manage.py createsuperuser*

### Database

In sviluppo viene utilizzato il database predefinito di Django con il suo nome standard “db.sqlite3”, lo stesso file è presente nella repository Github insieme ad un dump Json dei dati che si chiama “dati_demo.json”. Per il deploy su Railway è stato utilizzato il database PostgreSQL.

Il file “db.sqlite3” e il file “dati_demo.json” presenti sulla repository Github contengono i seguento dati di demo:
* 7 account (1 superadmin, 3 redattori, 3 fruitori)
* 21 eventi nei vari stati (futuro, passato, pubblicato, spubblicato, annullato)
* 11 tipologie di evento
* 11 prenotazioni

Con gli stessi dati è stato popolato il db PostgreSQL su Railway ma sono stati modificati durante prove successive.

### Demo account

Gli account demo già attivi sulla versione presentata sono:

| Username | Password | Ruolo |
| :--- | :--- | :--- |
| admin | django.20.26! | Amministratore |
| editor1 | pwd.ed@2026-1 | Redattore |
| editor2 | pwd.ed@2026-2 | Redattore |
| editor3 | pwd.ed@2026-3 | Redattore |
| utente1 | pwd@2026-1 | Fruitore |
| utente2 | pwd@2026-2 | Fruitore |
| utente3 | pwd@2026-3 | Fruitore |
| utente4 | pwd@2026-4 | Fruitore |

### Link di deployment

Per il rilascio dell’applicativo è stata scelta la piattaforma Railway, è raggiungibile al seguente link:  
https://gestione-eventi.up.railway.app/

---

## Scenari di test

Di seguito sono descritti brevemente alcuni scenari utili a testare le principali funzionalità del sistema:

### 1. Consultazione eventi
* **Azioni**
  1. accesso con utente1
  2. vago su “Tutti gli eventi”
  3. clicco sulla tipologia “Musica” per filtrare gli eventi di musica
  4. clicco sull’evento “Dario Cecchini - Soul Check”
* **Risultati**
  1. visualizzo la scheda di dettaglio dell’evento con la possibilità di prenotare

### 2. Prenotazione evento
* **Azioni**
  1. accesso con utente1
  2. Sulla home, nella sezione “I prossimi 6 eventi in programma” clicco su evento “Escursione alla Rasa con pranzo”
  3. Clicco sul bottona “Prenota”
* **Risultati**
  1. messaggio conferma prenotazione
  2. posti disponibili diminuito di 1
  3. posti prenotati aumentato di 1
  4. avviso evento già prenotato
  5. possibilità di cancellare la prenotazione

### 3. Eliminazione prenotazione su evento annullato
* **Azioni**
  1. accesso con utente1
  2. vago su “Eventi prenotati” dove trovo un messaggio di avviso della presenza di un evento prenotato annullato
  3. Clicco sull’evento annullato dall’avviso o dalla card
  4. Clicco su “Cancella prenotazione”
* **Risultati**
  1. messaggio conferma cancellazione
  2. posti disponibili aumentato di 1
  3. posti prenotati diminuito di 1
  4. non è più possibile prenotare l’evento perché è nello stato “annullato”

### 4. Consultazione prenotazioni
* **Azioni**
  1. accesso con utente1
  2. vago su “Eventi prenotati”
* **Risultati**
  1. arrivo su una pagina in cui visualizzo tutte le mie prenotazioni, quelle degli eventi futuri e quelle degli eventi passati

### 5. Inserimento evento
* **Azioni**
  1. accedo con l’utente editor1
  2. apro il menu utente cliccando sul bottone con il nome utente
  3. clicco su “Aggiungi evento”
  4. inserisco i dati dell’evento (immagine dimensione 500x350)
  5. seleziono l’opzione “Pubblicato”
  6. clicco su “Salva”
* **Risultati**
  1. creazione scheda di dettaglio dell’evento con messaggio conferma inserimento
  2. evento visualizzato tra gli eventi pubblicati sulla piattaforma

### 6. Eliminazione evento
* **Azioni**
  1. accedo con l’utente editor1
  2. vago su “Tutti gli eventi”
  3. clicco su “Pagina 2”
  4. clicco su evento “Fabrizio Fontana”
  5. clicco su “Elimina evento”
  6. clicco su “Si elimina”
* **Risultati**
  1. torno sulla pagina di tutti gli eventi con un “messaggio di conferma eliminazione”
  2. evento non più presente nel database

### 7. Eliminazione evento con prenotazioni
* **Azioni**
  1. accedo con l’utente editor1
  2. vago su “Tutti gli eventi”
  3. clicco su evento “Bugonia”
* **Risultati**
  1. nella scheda di dettaglio dell’evento appare un messaggio “Evento non eliminabile! Sono attive n. 3 prenotazioni.”

### 8. Spubblicazione evento con prenotazioni
* **Azioni**
  1. accedo con l’utente editor1
  2. vago su “Tutti gli eventi”
  3. clicco su evento “Amleto, tutto quello che non so”
  4. clicco su “Modifica evento”
  5. deseleziono l’opzione “Pubblicato”
  6. clicco su “Salva”
* **Risultati**
  1. torno sulla scheda dell’evento con un messaggio in alto “Impossibile spubblicare 'Amleto, tutto quello che non so': ci sono 2 prenotazioni attive. È possibile solo annullare l'evento”

### 9. Annullamento evento
* **Azioni**
  1. accedo con l’utente editor1
  2. apro il menu utente cliccando sul bottone con il nome utente
  3. clicco su “Gestione eventi”
  4. clicco sull’evento “Bugonia”
  5. clicco su “Modifica evento”
  6. seleziono l’opzione “Annullato”
  7. clicco su “Salva”
* **Risultati**
  1. torno sulla scheda dell’evento con il messaggio di conferma modifica
  2. Accanto al titolo appare la scritta “messaggio annullato”
  3. Negli elenchi, nella card dell’evento appare la scritta messaggio annullato
  4. Nella home e nella pagina delle prenotazioni dell’utente1 appare un messaggio che avvisa che l’evento è stato spubblicato

### 10. Consultazione prenotazioni su evento
* **Azioni**
  1. accedo con l’utente editor1
  2. apro il menu utente cliccando sul bottone con il nome utente
  3. clicco su “Gestione eventi”
  4. accanto alle informazioni su Posti disponibili e posti prenotati clicco sul link “Dettaglio prenotazioni”
* **Risultati**
  1. arrivo sulla pagina con l’elenco di tutte le prenotazioni attive su quell’evento con la possibilità di cancellarle

### 11. Aggiunta tipologia e modifica tipologia
* Le azioni e i risultati sono simili a quelli per gli eventi. L’unica differenza è che le tipologie già inserite si vedono direttamente nella maschera di inserimento ed è possibile solo modificare (non cancellare) le tipologie inserite da noi
