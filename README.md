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

## Domande

Q: come si integra nei sistemi di monitoraggio?

A: ...

Q: come si fa il failover?

A:

Q: come si scala?

A:

Q: E' possibile fare un sistema di messaggistica distribuito usando un RabbitMQ master che smista ad altri RabbitMQ?

A:
