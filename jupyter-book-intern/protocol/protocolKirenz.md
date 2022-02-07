# Protokoll - Sprechstunde Kirenz

## Kickoff Termin am 23.09.2021

### Die Aufgabe:

- Unsere Aufgabe ist es genau einen Use Case abzubilden der vorher fest definiert ist. Dieser Use Case soll möglichst den ganzen Prozess durchlaufen, alles was von dem Use Case nicht abgedeckt wird soll trotzdem implementierbar sein
- Das zu entwickelnde Framework sollte unabhängig vom Use Case möglichst generisch und skalierbar sein. Der Use Case sollte also vom Framework abgedeckt werden können, das Framework soll aber auch möglichst alle anderen Use Cases abdecken, sprich: Die Möglichkeit anhand des zugrundeliegenden Konzepts das wir uns ausgedacht haben sollte bestehen. Beispiel: In unserem Use Case werden nur Streaming-Daten verwendet. Es sollte allerdings möglich sein Batch-Daten auch zu nutzen im Rahmen unserer entwickelten Lösung.
- Man sollte versuchen in einem ganzheitlichen System zu denken. Die von uns entwickelte Gesamtlösung sollte dem MLOPs-Gedanken entsprechen.
- Die Lösung soll skalierbar sein!! -> sehr oft erwähnt
- Der Use Case sollte am besten noch Besonderheiten haben die andere Use Cases nicht haben. Er sollte anhand des vorgestellten Life Cycles umsetzbar sein.
- Eine Implementierung der skizzierten Lösung ist auf jeden Fall zwingend notwendig und Teil der Aufgabe. Bosch ist auch an den eingesetzten Technologiekomponenten interessiert.
- Das Deployment der implementierten Lösung ist zu überlegen wie tiefgreifend wir das umsetzen wollen. Auch hier können wir Schwerpunkte setzen.
- MLOPs ist ein generalisiertes System, mit dem man ein großes Feld (im Idealfall alle Use Cases) ausführen kann im Rahmen eines generalisierten Frameworks
- Wir sollen recherchieren was es an Best Practice Ansätzen gibt.

Zusammenfassung:

- Schwerpunkte können gesetzt werden, aber man sollte die Möglichkeit haben alles weiter benötigte hinzuzufügen (siehe Beispiel Streaming/Batch-Daten)

### Weitere Informationen

- Beim Modell kann man sich eins aussuchen. Das war ihm nicht so wichtig. Wir sollen eher schauen welche Modelle sich am besten implementieren lassen und ressourcenschonend sind. Das ist wichtiger als die reine Performance der Modelle (also ob ein Modell jetzt 1% genauer als das andere ist). Der Prozess soll möglichst praxisrelevant sein.
- Wir sollen uns TFX von Tensorflow (Google) anschauen, das gibt es seit diesem Mai und ist so der Favorit der Szene und gerade State of the Art. Kann sehr leicht implementiert werden.
- Wir sollen uns die Apply Konferenz ansehen. Da stellen Unternehmen ihre Best Practice Lösungen in dem Bereich vor.

### Feedback zu unseren Ideen

#### Börsendaten

- Er ist skeptisch ob das wirklich funktioniert, da es schwer ist da allgemeine Trends auszuwerten. Das ist allerdings auch nicht der Fokus des Kurses, deshalb fände er es auch nicht schlimm wenn wir das als Use Case verwenden und schlechte Ergebnisse hätten. Merke: Es spielt keine Rolle ob das Modell eine schlechte Performance hat.
- Was ihm gefallen hat war das wir da leicht an Daten kommen könnten, wir müssten diese nicht von Hand generieren. Die Frage wäre da dann hauptsächlich wie wir die Daten ablegen.
- Ihm gefällt der Vorschlag mit den Börsendaten am besten (hauptsächlich wegen den Streaming-Daten). Es wäre cool wenn wir einen anderen Use Case in der Richtung finden, der nicht unbedingt Aktienkurse mit einbezieht, da es wie gesagt schwer ist das vorherzusagen.

#### Wetterdaten

- Kann man kombinieren mit der Idee zu den Börsendaten. Dann könnte man auch noch andere Datenquellen mit reinnehmen: z.B. Nachrichten etc.

#### Bewerbungen

- Die Idee fand er auch interessant, findet es aber schwierig das man keine vorher definierten Label hat (wie haben keine abhängige Variable, wir müssten fiktive Daten für erfolgreiche und nicht erfolgreiche Matches erstellen). Es ist also schwierig zu bewerten ob der Bewerber passend ist.
- Bei LinkedIn wäre zusätzlich noch das Problem, dass man nur die Daten aus seinem eigenen Netzwerk sehen kann.

#### Lose Gedanken

- Am besten sollten wir uns einen Use Case raussuchen bei dem man gut an Daten gelangt. Er ist nicht so der Fan davon Daten selber zu generieren.
- Für Dashboards sollen wir uns mal Frameworks von React anschauen. Das sollten wir eher ergänzend zu unseren Ideen nutzen
- Das folgende hab ich notiert aber weiß nichtmehr was ich damit gemeint habe: Herkunft der Daten: Würde sehr gut passen. Data Mesh anschauen, da geht es auch darum dass man die Herkunft der Daten kennt.
- Es muss Möglichkeiten geben, die Daten zu bereinigen. Es wäre cool wenn es eine Art Transform-Einheit gäbe, aber das müssten wir nicht unbedingt selbst implementieren, sondern kann auch Mock-Mäßig eingebunden sein. Es kommt darauf an wie wir die Schwerpunkte setzen.

#### Was Kirenz noch von uns Wissen möchte

- Er würde würde Workshops zu Schwerpunktthemen geben, da müssen wir ihm sagen wo wir noch Unterstützung/Input brauchen
- Bis zum Termin am 6. Oktober sollte man sich auf einen konkreten Vorschlag eines Use Cases festlegen.
- Man soll festlegen was die Schwerpunkte sind und wer sich innerhalb der Gruppe mit was beschäftigt (trotzdem soll sich jeder in der Gruppe mit dem Gesamtsystem auskennen). Das ist hauptsächlich für die Bewertung für ihn geschickt.

#### Besprechung der Gruppe

- Die Gruppe trifft sich am 4. Oktober abends nochmal zwecks möglicher Themen etc. Bis dahin sollte jeder einen groben Plan haben in welche Richtung es gehen soll.

## Meeting 06.10.2021

- Bosch interessiert vor allem auch die Frage: "Wie kann man mit den Daten systematisch umgehen?", z.B. Metadatenmanagement

### Empfohlenes Vorgehen

Prinzipiell sollen wir am besten Delta Lake nutzen. Dort gibt es eine Schritt-Für-Schritt-Anleitung für den ganzen Prozess

### Delta Lake

- Ist Open Source
- State of the Art bei MLOPs

Vorgehen:

- In Erfahrung bringen welche Daten wir nutzen können
- Daten als batch abziehen und dann eine Technologie nutzen um daraus bewegte Daten zu simulieren (Apache Airflow/Nifi)
- In welcher Form speichere ich die Daten ab (Lakehouse -> Apache HBase anschauen, das ist eine Open Source Alternative zu BigQuery)
- Wie gestalte ich das Metadatenmanagement
- Wie werden die Daten bereit gestellt

Das gesamte Vorgehen ist von Delta Lake abgebildet. Deshalb hat er das auf jeden Fall empfohlen. Wenn man Delta Lake nicht nutzt muss man das alles selber implementieren/entwickeln

### Sonstiges

- Modell muss nicht nutzbar für 10 verschiedene Use Cases sein. Es geht darum, eine Systemarchitektur aufzubauen in der man einzelne Bausteine austauschen kann. Die Pipeline selbst soll dabei weitestgehend automatisiert sein.
- Wir sollen am besten eine Datenquelle mit Kriminalitätsdaten aus Deutschland finden!!
- Zum Deployment: Am besten TFX (von Google) anschauen. Dort gibt es mehrere Optionen für das Deployment. Kubeflow kann auch den gesamten Prozess abbilden, das ist auch schon mit Kubernetes verbunden und deshalb beliebig skalierbar
- Für die Dashboards sollen wir Plotly (auf React-Basis) nutzen. Das ist HTML basiert und deshalb besser als matplotlib

## Meeting 20.10.2021

- Dokumentation auf englisch ist okay
- Jupyter Books für Dokumentation verwenden
- Argo ist eher für Deployment, kann in Kombination mit Apache Airflow verwendet werden

## Meeting 24.11.2021

### Data exploration (Datenveredelung)

- Broze: Saubere Daten

- Gold: Gold sind Daten die bereits aufbereitet wurdem:
  
  - Durchschnitte wurden gebildet
  
  - Cluster etc.

- Um Daten besser labeln zu können, kann der smote Algorithmus verwendet werden --> mal anschauen!

- Nützliche Links
  
  - [First steps in pandas &#8212; Introduction to pandas](https://kirenz.github.io/pandas/pandas-intro-short.html)

- Für die grpahische Darstellung eignet sich sehr gut maps api, um die locations usw. zu bestimmen. Daten nach Orte zu untersuchen 
  
  - Cluster mit Stadt, District etc. kann so gebildet werden

### Termin mit Bosch

- Ist in erster Linie damit wir offene Fragen klären können
  
  - Architekturfragen
  
  - Datenhaltungsfragen

- Termin ist eher als Feedback gedacht

- Können hier bereits Sachen vorstellen müssen dies aber nicht tun

- Allg. Fragen zur Implementierung können gestellt werden

- Wichtig! Theorie sollte zu diesem Termin sitzen 

### Nächste Schritte

- Modell mit Tensorflow erstellen

- Dash können wir erstmal ausklammern. Wichtiger ist das MLOPS Prozess steht und wir inhatlich alles verstanden haben 

### Nützliche Links

- http://www.feat.engineering/

## Meeting 22.12.2021

- Delta Lake = realtive pfade können nicht gelesen werden

- Lösung wie wir es gemacht haben gut aber zu zeitintesiv das jetzt noch in das richtige Format zu bekommen. Könnten nur nochmal probieren, ob es funktioniert wenn wir es nicht in ein dataframe sondern in eine json schreiben. 
  Ansonsten:
  
  - Daten von API fetchen und lokal in json ablegen
  
  - Json dann in DataFrame in Spark einlesen

### Schnittstelle DeltaLake/TFX

Schnittstelle schwierig da nur bestimmte Dateiformate von TFX unterstützt werden. 

**Lösung: ** CSV exportieren aus dem DeltaLake und lokal bereitstellen. Diese dann einfach in TFX einlesen und so weiterarbeiten. Harter Cut zwischen den zwei Technologien so i.O.

## Meeting 12.01.2022

### Feature Store

Kein Unterschied zwischen Trainings und Serving Daten, daher wird Feature Store angewendet. Müsste in realer Welt eine Art Feedback Loop von dem bereitgestellten Model zu den Trainingsdaten geben. „Retrain Triggers“ in MLOps Prozess.

Bsp. Saisonale Unterschiede bei Daten, Sommer vs Winter Daten im Kleidungshandel.
Datenkatalog in unserem Fall ausreichend. Dies wird über Delta Lake realisiert. Nicht so sehr im Fokus. Beschriftung der Daten ausreichend.

=> Kommentar Niklas: Kein weiterer Handlungsbedarf.

In der Doku dokumentieren welche Daten wir verwendet haben etc.

### Metadatenmanagement

**Nur Metadaten in TFX? Nein beides, da zwei Welten:**

- Delta Lake ist Spark basiert.

- TFX kann damit nicht umgehen.

- Spark MLib, wäre bei großen Daten dann einfacher.

- Cut zw. Delta-Lake und MLOps „Logik“. TFX MLMD Meta Datastore, der lebt außerhalb vom Delta-Lake.

- Delta Lake passt so wie wir es haben Daten. Einfach gold daten in eigene Tabelle. 

**Graphische Oberfläche nötig oder reicht Metadaten-Management in einer DB?**

Je nachdem wie das Artefakt aussieht dass ein Modul erstellt, ist der Zugriff eben unterschiedlich.

Visualisierungen im Tensorboard + Visualisierung in der Data Validation => kann auch für die Präsentation dann verwendet werden

Um alles nachvollziehbar zu halten, wann sind welche Daten angeliefert worden und wie sollen die Grenzwerte bspw. aussehen. 

Überlegen was in Airflow und was in MLData geloggt wird und strategie erklären. Mögliches Szenario. Airflow sehr hohe FLughöhe des Loggins, da dies eher als Management tool genutzt wird und MLMD dann sehr granular, sodass die entwickler dies dann zum debuggen verwenden können

=> Idee ausarbeiten und in Doku darstellen 

### Wo Artifakte ablegen?

Hier überlegen ob in einem eignen S3 Bucket oder zurück in Delta Lake schreiben. Eigener S3 Bucket für Kirenz ok. Vielleicht nochmals gedanken machen und in Doku begründen warum wir das so gemacht haben oder alternativen aufzeigen

### Noch ausstehende Dinge:

- Delta Lake so i.O. wie wir es haben. Müssen wir nichts mehr ergänzen

- TFX Komponenten weitestgehend abgedeckt, das ist gut!

- Zusätzlich noch Deployment, dann wärs mega:
  
  - Wie macht man das Serving?

- Visualisierung in Form eines Dashboards ausreichend, vielleicht auch nur konzeptionell.

Zusammengefast: Sind auf einem guten Weg. Wenn wir das so zu Ende bringen ok

### Termin mit Bosch

Können im Prinzip die gleichen Fragen stellen wie beim heutigen Termin. Hier nochmals die Fragen: 

- Metadatenmanagement ([ML Metadata &nbsp;|&nbsp; TFX &nbsp;|&nbsp; TensorFlow](https://www.tensorflow.org/tfx/guide/mlmd "https://www.tensorflow.org/tfx/guide/mlmd"))
  --> Wie am besten umsetzten? 
  ---> Wo werden die Daten dann visualisiert (wäre das unser Dashboard)
  --> Ergebnis des Models kann dann auch hieraus ausgelesen werden oder?
- Wie sieht der Termin aus was sollen wir bis dahin vorbereiten?
  --> Was sind die wichtigsten Punkte für Bosch (Metadatenmanagement)
- Feature Store 
  Wie viel Aufwand da investieren? Eigentlich ja das gleich wie unser "gold" standard den wir in einen 
  extra table geschrieben haben 
  ([Databricks Feature AWS Store Quickstart](https://examples.hopsworks.ai/master/featurestore/databricks/featurestorequickstartdatabricksaws/ "https://examples.hopsworks.ai/master/featurestore/databricks/featurestorequickstartdatabricksaws/"))
- Delta Lake (soweit fertig - ggf. Feature Store)
- tfx (bis Example Validator läuft --> voll fertigstellen)
  --> Metadatenmanagement ( Wie viel müssen wir machen und was?) (Bearbeitet)

## 
