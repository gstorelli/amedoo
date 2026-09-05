# A.M.E.D.O.O. — Sito Ufficiale

Sito istituzionale dell'**Associazione Meridionale Estimatori e Degustatori dell'Olio di Oliva** di Bari, associazione senza fini di lucro fondata nel 1992 presso la Camera di Commercio di Bari.

Pubblicato con **GitHub Pages** → https://gstorelli.github.io/amedoo/

## Contenuti

- **Chi Siamo** — storia dell'associazione e partner istituzionali (Camera di Commercio di Bari, Unioncamere Puglia, SAMER, AIS Puglia)
- **L'Arte dell'Assaggio** — perché diventare assaggiatore
- **Il Metodo Panel Test** — il panel test ufficiale a norma COI
- **Sensory Profiler** — strumento interattivo di analisi sensoriale
- **Corsi & Certificazioni** — corso di Idoneità Fisiologica all'Assaggio (MASAF), masterclass e panel
- **Statuto** — [statuto_amedoo.pdf](./statuto_amedoo.pdf), versione digitale solo-testo (24KB) con statuto e regolamenti dei corsi

## Struttura

```
amedoo/
├── index.html                          # pagina unica (SPA-like, Tailwind via CDN)
├── statuto_amedoo.pdf                  # statuto digitalizzato (OCR + revisione)
├── logo.png                            # logo ufficiale orizzontale (trasparente)
├── logo_gold.png                       # variante oro per footer scuro
├── logo-mark.png                       # mark quadrato (favicon, avatar)
├── partner_*.png                       # loghi partner istituzionali
├── hero_tasting.webp                   # foto sezione hero
├── monumental_grove.webp               # ulivi monumentali
├── panel_lab.webp                      # laboratorio panel test
└── culinary_pairing.webp               # abbinamento cibo-olio
```

## Peso e performance

Ottimizzato per il web: **~0.8MB totale** di asset (foto in WebP, loghi PNG quantizzati a 256 colori, statuto vettoriale). Nessuna dipendenza da build: HTML statico con Tailwind CDN e Lucide Icons.

## Pubblicazione

Il sito si pubblica su branch `main` tramite GitHub Pages (Settings → Pages → Source: `main` / root). Ogni push su `main` aggiorna il sito.

## Contatti

- **Sede**: c/o Camera di Commercio di Bari, Corso Cavour 2 / Via E. Mola 19 — 70121 Bari
- **Email**: info@amedoo.it
- **PEC**: amedoo@pec.it
- **Instagram**: [@amedoo_bari](https://www.instagram.com/amedoo_bari/)
