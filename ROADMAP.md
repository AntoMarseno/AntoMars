# ALLINEA — Roadmap

## Adesso (in corso)
- [URGENTE sicurezza] Svuotare la chiave Google in config.js e eliminarla dalla console Google Cloud. La voce ha gia il fallback su Web Speech, non serve.
- Layout camera a tutto schermo: object-fit cover su webcam e canvas, per verticalita e niente spazio vuoto. (in test)
- Affidabilita rilevamento: funzione reliable() su frame bounds, la posa non e valida se le gambe non sono viste. (appena messo)
- Tarare dal vivo FRAME_MARGIN (0.02) e MIN_VIS (0.6).
- Pulire codice morto ZOOM_SCALE.

## Prossimo (dopo che il core regge)
- Spostare il feedback sulla voce di Astrid come canale primario; schermo solo a colpo d'occhio, stati grandi ad alto contrasto leggibili da 3 metri.
- Onboarding inquadratura: overlay sagoma "entra nel riquadro", telefono in basso angolato verso l'alto.
- Inquadratura per-posa: misurare solo gli angoli che contano per ogni posa, cosi l'utente sta piu vicino.
- Lista d'attesa email + analytics base per la validazione.

## Piu avanti / app nativa
- Grandangolo via lente ultra-wide per ridurre la distanza: non fattibile da browser, sì in nativo.
- Correzione distorsione lente se si usa l'ultra-wide.
- Pose detection real-time on-device performante iOS/Android, backend, abbonamenti, store.
- Cattura in portrait nativo per ridurre il crop laterale.

## Decisioni parcheggiate
- Cercare CTO con profilo ML/computer vision solo dopo la validazione, da posizione di forza. Niente equity prima del segnale. Per la demo eventualmente un freelance tecnico a progetto.
