# A.M.E.D.O.O. — Sito Ufficiale

Sito istituzionale dell'**Associazione Meridionale Estimatori e Degustatori dell'Olio di Oliva** di Bari, associazione senza fini di lucro fondata nel 1992 presso la Camera di Commercio di Bari.

Pubblicato su **https://associazioneamedoo.it** (VPS Contabo, Docker + nginx-proxy). GitHub Pages non è più utilizzato.

## Contenuti

- **Chi Siamo** — storia dell'associazione e partner istituzionali (Camera di Commercio di Bari, SAMER Lab)
- **L'Arte dell'Assaggio** — perché diventare assaggiatore
- **Il Metodo Panel Test** — il panel test ufficiale a norma COI
- **Sensory Profiler** — strumento interattivo di analisi sensoriale
- **Corsi & Certificazioni** — Idoneità Fisiologica all'Assaggio (MASAF), Masterclass abbinamento cibo-olio, 20 Sedute Certificate, Addestramento e Perfezionamento Continuo
- **Statuto** — [statuto_amedoo.pdf](./statuto_amedoo.pdf), versione digitale solo-testo con statuto e regolamenti dei corsi

## Struttura

```
amedoo/
├── index.html                 # pagina unica (Tailwind via CDN, nessuna build)
├── contenuti.esempio.json     # testi editabili: copia iniziale (seed)
├── statuto_amedoo.pdf         # statuto digitalizzato (testo selezionabile)
├── logo.png / logo_gold.png   # logo ufficiale e variante per footer scuro
├── logo-mark.png              # mark quadrato (favicon, avatar)
├── partner_*.png              # loghi partner istituzionali
├── *.webp                     # fotografie ottimizzate
├── admin/                     # area riservata per modificare i testi
├── deploy/                    # configurazione nginx + script di avvio
├── Dockerfile                 # immagine del sito (nginx:alpine)
└── docker-compose.yml         # sito + area riservata dietro nginx-proxy
```

## Modificare i testi (area riservata)

I testi più soggetti a cambiamenti (sessione corsi, contenuti delle card dei corsi, contatti, sedi, citazione, descrizione nel footer) sono marcati in `index.html` con `data-cms="chiave"` e possono essere modificati online senza toccare il codice.

- **Indirizzo**: `https://associazioneamedoo.it/gestione` (login e password in `.env`, variabili `ADMIN_USER` / `ADMIN_PASSWORD`)
- Sta sullo stesso dominio del sito: **nessun sottodominio, nessun record DNS aggiuntivo**. Il container `web` inoltra `/gestione/` al container `admin`
- Le modifiche sono salvate in `contenuti.json` e visibili **subito** al refresh del sito, senza rebuild
- Se `contenuti.json` manca o è vuoto, il sito mostra i testi presenti nell'HTML: nessun rischio di pagina vuota
- La pagina dell'area riservata è esclusa dai motori di ricerca (`X-Robots-Tag: noindex`)
- Per interruzioni di layout o nuove sezioni serve invece una modifica al codice

## Form contatti e newsletter

I form non hanno backend: al submit compongono una **email precompilata** (`mailto:`) con oggetto e corpo già scritti e la aprono nel programma di posta dell'utente, indirizzata alla segreteria. Il destinatario è la chiave `contatti.email` in `contenuti.json` (usata anche dal footer).

## Deploy sul VPS (Contabo + nginx-proxy)

Prerequisiti: Docker + Compose, reverse proxy `nginx-proxy` (jwilder) con `acme-companion` attivi, rete Docker del proxy esistente.

```bash
git clone https://github.com/gstorelli/amedoo.git && cd amedoo
cp .env.example .env      # imposta PROXY_NETWORK, ADMIN_PASSWORD e (se serve) ADMIN_PATH
sh deploy/avvia.sh        # crea contenuti.json e avvia sito + area riservata
```

DNS necessario (unico record A verso l'IP del VPS):

| Dominio | Uso |
|---|---|
| `associazioneamedoo.it` | sito + area riservata su `/gestione` (nginx-proxy + certificato Let's Encrypt automatico) |
| `www.associazioneamedoo.it` | alias del sito |

Aggiornare dopo una modifica al codice:

```bash
git pull && docker compose up -d --build
```

Note operative:

- `VIRTUAL_HOST` / `LETSENCRYPT_HOST` pilotano nginx-proxy e acme-companion: non serve modificare la loro configurazione
- Solo i file del sito entrano nell'immagine (`.dockerignore` esclude git, documenti di lavoro e asset non usati)
- `contenuti.json` **non è versionato** (è in `.gitignore`): vive solo sul VPS, così i `git pull` non vanno mai in conflitto con i testi modificati dall'area riservata
- Healthcheck: `https://associazioneamedoo.it/healthz`

## Peso e performance

**~0.8MB** di asset totali: fotografie in WebP, loghi PNG quantizzati, statuto vettoriale. Nessuna build: HTML statico con Tailwind CDN, Lucide Icons e GSAP. Il container nginx serve con gzip, cache lunga per immagini e rivalidazione per l'HTML.

## Contatti

- **Sede legale**: Corso Cavour 2 — 70121 Bari (BA)
- **Sede operativa**: Via E. Mola 19 — 70121 Bari (BA)
- **Email**: segreteriaamedoo@gmail.com
- **PEC**: amedoo@pec.it
- **Instagram**: [@amedoo_bari](https://www.instagram.com/amedoo_bari/)
