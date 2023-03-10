# IDI 2023 - Rabbit MQ by Coders 51

Docenti:

- Gianluca Padovani
- Emilio Francischetti

## About this repo

To start RabbitMQ using docker, run the following command:

```bash
make fg
```

Stop it with CTRL+C.

You can start/stop it in background with:

```bash
make start
make stop
```

L'interfaccia web e' disponibile su <http://localhost:15672/>.
Per autenticarsi l'account di default e' `guest`/`guest`.

## RabbitMQ vs Kafka

Kafka si definisce come uno stream processing platform, mentre RabbitMQ è un message broker.

Kafka è stato progettato per essere scalabile, mentre RabbitMQ è stato progettato per essere semplice.

## Intro su RabbitMQ

RabbitMQ e' molto semplice e flessibile ed e' uno dei sistemi di messaggistica piu' usati (nella top ten di download di docker hub)

Messaggi di RabbitMQ sono sempre binari, non possono essere stringhe.
Ci possiamo mettere dentro quello che vogliamo, solo recentemente sono stati limitati in dimensione.

I messaggi vengono inviati a un exchange che e' connesso a una o piu' code.

## Lessico

**Broker**: e' il server che gestisce le code e gli exchange, ovvero il nostro RabbitMQ.

**Producer**: e' il processo che invia messaggi agli exchange.

**Consumer**: e' il processo che riceve messaggi dalle code.

**Binding**: e' la connessione tra un exchange e una coda. Il binding puo' essere configurato in diversi modi.

Ci possono esssere piu' consumers che leggono dalla stessa coda o un consumer puo' leggere da piu' code.
Di default RabbitMQ invia i messaggi ai consumers in modo round-robin.
Si puo' anche modificare RabbitMQ per inviare i messaggi solo alle code che non sono impegnate.
Si puo' anche fare in modo che lo stesso messaggio vada a tutti i consumers che leggono dalla coda.

A seconda delle situazioni si puo' voloere avere piu' connessioni (che implica piu' rapidita') oppure meno connessioni (che implica meno overhead per RabbitMQ).

Quando RabbitMQ sta bene di solito non ha messaggi in coda.
Se ne ha molti e fatica a smistarli, vuol dire che qualcosa non va.
Magari si possono aggiungere piu' consumers.

Chi governa il round-bobin e' il parametro `prefetch_count` del consumer.

Il round robin e' sui consumer a cui vengono inviati un numero di messaggi pari al `prefetch_count` per poi passare al prossimo.
Se c'e' molto parallelismo, il prefetch deve essere alto.
Se invece i processi vanno serializzati, il `prefetch_count` puo' essere anche 1.
Se il `prefetch_count` e' 0 si rischia che al riavvio del consumer si prenda carico di un numero troppo elevato di messaggi.

## Esempi

Nella cartella `src/exercises` ci sono un po' di esercizi.

### Esercizio 1: Exchange di tipo direct

Gli exchange direct sono quelli piu' semplici e veloci.

Abbiamo un `producer.py` che invia ogni secondo un messaggio ad un exchange di tipo direct con una routing key a caso tra `info`, `warning`, `error`.

Abbiamo un `consumer.py` che legge da un exchange di tipo direct con routing le routing key passate come argomento.

Ad esempio:

```bash
src/exercises/1$ python consumer.py info warning
```

Se nessun parametro viene passato, il consumer assume una routing key di tipo info.

### Esercizio 2: Exchange di tipo fanout

Abbiamo un `producer.py` che invia ogni secondo un messaggio ad un exchange di tipo fanout.

Tutti i consumers ricevono tutti i messaggi.

Lo svantaggio e' che:

- la routing key non viene usata
- RabbitMQ puo' andare in crisi se deve creare o distruggere molte code

### Differenza tra durable e auto_delete

Le code con `auto_delete` vengono distrutte quando non ci sono piu' consumers che leggono da quelle code.

Le code con `durable` vengono salvate su disco e non vengono distrutte quando RabbitMQ viene riavviato, altrimenti andrebbero perse.

### Esercizio 3: Exchange di tipo topic

Gli exchange di tipo topic sono molto potenti e flessibili.
Assomigliano ai direct ma e' possibile usare dei caratteri speciali per fare match di routing key.
RabbitMQ si aspetta rounting keys separate da `.`.

I caratteri speciali `*` e `#` possono essere usati per filtrare sottoparti della routing key.
Il carattere `*` matcha una sottoparte della routing key, mentre il carattere `#` matcha tutte le sottoparti rimanenti della routing key.

Per esempio `foo.*` matcha `foo.bar` *ma non* `foo.bar.baz`.
Per esempio `foo.#` matcha `foo.bar` *e* `foo.bar.baz`.
Nota che `foo#` non matcha ne' `foo` ne' `foo.bar`.'
Nota che `foo.*.#` matcha `foo.bar` e `foo.bar.baz.buz`.

*N.B.*: c'e' un limite di 255 byte sulla routing key.

### Parametri delle code

**Lazy**: se e' attivo RabbitMQ non tiene i messaggi in memoria ma li salva su disco.
Utile per code di debug o per code da processare in un secondo momento con un batch (modalita' di utilizzo di RabbitMQ sconsigliata).

**Max length**: se e' attivo RabbitMQ immagazina al massimo un certo numero di messaggi nella coda.
Ci sono diversi modi per gestire l'overflow, ma lo standard e' di scartare i messaggi piu' vecchi quando l'N+1-esimo messaggio arriva.

**Max length bytes**: come sopra ma si misura la dimensione dei messaggi in byte.

### Modalita' di utilizzo di consumo

**auto ack**: il messaggio viene rimosso dalla coda appena e' stato processato.
Se il consumer va in errore il messaggio viene perso.
Si consiglia di evitarlo.

### Cosa fare se il consumer va in errore

Supponendo di non avere l'auto ack, il messaggio viene rimosso dalla coda solo se il consumer invia un ack.
Se il consumer va in errore il messaggio viene rimesso in coda.
Si puo' fare dando a RabbitMQ un `nack` invece di un `ack`.
RabbitMQ ti dice se il messaggio e' stato "Redelivered" in seguito ad un *nack*.

### Esercizio 4: ack e nack

La funzione di callback del consumer se riceve un messaggio manda un nack se non e' redelivered, altrimenti manda un ack.

Esistono code di tipo quorum che tengono il conto delle volte che un messaggio e' stato processato.
Le code di tipo quorum hanno anche la possibilita' di limitare il numero di retry per coda (delivery limit).

Il problema e' che se questo e' impostato sulla coda poi non e' piu' modificabile.

Il problema puo' essere risolto applicando una policy.

Le policy si possono applicare sia alle code che agli exchange.

### Messaggi scartati

Se un messaggio viene scartato, RabbitMQ lo invia ad un exchange di tipo dead letter exchange che potrebbe non essere impostato.

E' sempre una buona idea avere un dead letter exchange per controllare che non ci siano messaggi scartati.
C'e' un altro caso in cui un messaggio viene scartato, ovvero quando un exchange non ha bindings con nessuna coda.
In questo caso si puo' configurare una policy che configura per l'exchange un alternate exchange.

### Esercizio 5: Dead letter exchange

Crea coda quorum con dead letter exchange.
Dopo 10 volte lo scarto.
Va ad un coda dead letter queue che ha il binding con dead letter exchange.

**Da completare**, prevede al configurazione manuale delle code e degli exchange.

...

### Gestire errori in fase di pubblicazione.
Puo' succdere che la connessione si interrompa mentre si sta pubblicando un messaggio.
In questo caso il messaggio viene perso.

In typescrict si fa un `channel.waitForConfirms()` che ritorna una promessa
che viene risolta quando il messaggio viene pubblicato.

In Python si usa `channel.confirm_delivery(callback)`.

### Code di tipo stream

Nascono da un lavoro della community.
Se consumo da quelle code ma accettano un parametro `x-stream-offset` che permette di specificare da dove iniziare a leggere.
Questo permette di avere messaggi persistenti che possono essere letti e riletti.
Volendo ci si puo' segnare da dove ripartire. Ci sono dei client specializzati che ricordano l'ultimo messaggio letto e fanno ripartire lo stream da lì.

Lo stream usa un protocollo diverso.

### Clustering

Occorre avere un cookie con cui le varie istanze di RabbitMQ si identificano.
E' uno standard erlang cookie.

Vedi https://github.com/coders51/rabbitmq-devops per un repo che crea un numero dispari di VMs con RabbitMQ in cluster.

### RabbitMQ monitoraggio

I parametri che interessano di piu' sono i messagge unacked e i messaggi in dead letter queue.

### RabbitMQ production checklist

Vedi https://www.rabbitmq.com/production-checklist.html

## Domande

Q: come si integra nei sistemi di monitoraggio?

A: Prometeus ha dei plugin per RabbitMQ.

Q: come si scala e fa failover?

A: Ci sono diversi modi per fare clustering. Da guardare lo shovel che permette di spostare messaggi da un cluster ad un altro.

Q: E' possibile fare un sistema di messaggistica distribuito usando un RabbitMQ master che smista ad altri RabbitMQ?

A: Si, si puo' fare con lo shovel.

Q. Qual e' il TTL di default di un messaggio?

A: E' impostato quando si crea la coda.

Q. E' possibile fare debouncing dei messaggi?

A: Con le code di tipo stream e' possibile gestire la deduplicazione con un plugin impostando un parametro, ma non il debouncing.
Il messaggi successivi al primo che hanno una certa proprieta' vengono scartati.
