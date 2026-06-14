# ALLINEA — Roadmap

## Le due priorita
Detection posturale affidabile e voce naturale di Astrid. Tutto il resto viene dopo che questi due reggono.

## Adesso (in corso)

Detection:
- Layout camera a tutto schermo: object-fit cover su webcam e canvas, per verticalita e niente spazio vuoto. (in test)
- Affidabilita: funzione reliable() su frame bounds, la posa non e valida se le gambe non sono viste. (appena messo)
- Tarare dal vivo FRAME_MARGIN (0.02) e MIN_VIS (0.6).

Voce:
- Clonare la voce di Astrid con ElevenLabs e generare le ~100 frasi pre-registrate, una tantum offline, esportate in MP3 e committate. Nessuna API a runtime.
- Rendere le frasi generiche, senza il nome utente. Il nome resta solo a schermo. Elimina l'unica ragione per cui serviva la TTS dinamica.
- Eliminare del tutto la chiave Google: svuotare config.js e cancellarla dalla console Google Cloud. Niente piu chiave esposta nel client.
- Liberatoria firmata da chi presta la voce (consenso esplicito, uso commerciale).
- Costo: generazione una tantum, rientra nel piano Starter di ElevenLabs (~5$/mese, licenza commerciale, clonazione istantanea da 1-2 min). Free tier solo per testare la qualita.

Pulizia:
- Rimuovere il codice morto ZOOM_SCALE.

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
- Voce: se servira pronunciare nomi arbitrari a runtime, proxy serverless (Cloudflare Workers) con la chiave lato server. Solo a scala, non ora.
- Qualita voce: valutare la Professional Voice Cloning di ElevenLabs (piano Creator, 30+ min di audio) per una resa superiore.

## Decisioni parcheggiate
- Cercare CTO con profilo ML/computer vision solo dopo la validazione, da posizione di forza. Niente equity prima del segnale. Per la demo eventualmente un freelance tecnico a progetto.
