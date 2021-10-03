# Kickoff Termin am 23.09.2021

## Die Aufgabe: 

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

## Weitere Informationen

- Beim Modell kann man sich eins aussuchen. Das war ihm nicht so wichtig. Wir sollen eher schauen welche Modelle sich am besten implementieren lassen und ressourcenschonend sind. Das ist wichtiger als die reine Performance der Modelle (also ob ein Modell jetzt 1% genauer als das andere ist). Der Prozess soll möglichst praxisrelevant sein. 
- Wir sollen uns TFX von Tensorflow (Google) anschauen, das gibt es seit diesem Mai und ist so der Favorit der Szene und gerade State of the Art. Kann sehr leicht implementiert werden. 
-  Wir sollen uns die Apply Konferenz ansehen. Da stellen Unternehmen ihre Best Practice Lösungen in dem Bereich vor. 

## Feedback zu unseren Ideen

### Börsendaten

- Er ist skeptisch ob das wirklich funktioniert, da es schwer ist da allgemeine Trends auszuwerten. Das ist allerdings auch nicht der Fokus des Kurses, deshalb fände er es auch nicht schlimm wenn wir das als Use Case verwenden und schlechte Ergebnisse hätten. Merke: Es spielt keine Rolle ob das Modell eine schlechte Performance hat.
- Was ihm gefallen hat war das wir da leicht an Daten kommen könnten, wir müssten diese nicht von Hand generieren. Die Frage wäre da dann hauptsächlich wie wir die Daten ablegen. 
- Ihm gefällt der Vorschlag mit den Börsendaten am besten (hauptsächlich wegen den Streaming-Daten). Es wäre cool wenn wir einen anderen Use Case in der Richtung finden, der nicht unbedingt Aktienkurse mit einbezieht, da es wie gesagt schwer ist das vorherzusagen. 

### Wetterdaten

- Kann man kombinieren mit der Idee zu den Börsendaten. Dann könnte man auch noch andere Datenquellen mit reinnehmen: z.B. Nachrichten etc. 

### Bewerbungen

- Die Idee fand er auch interessant, findet es aber schwierig das man keine vorher definierten Label hat (wie haben keine abhängige Variable, wir müssten fiktive Daten für erfolgreiche und nicht erfolgreiche Matches erstellen). Es ist also schwierig zu bewerten ob der Bewerber passend ist. 
- Bei LinkedIn wäre zusätzlich noch das Problem, dass man nur die Daten aus seinem eigenen Netzwerk sehen kann. 
- 

#### Lose Gedanken 

- Am besten sollten wir uns einen Use Case raussuchen bei dem man gut an Daten gelangt. Er ist nicht so der Fan davon Daten selber zu generieren. 
- Für Dashboards sollen wir uns mal Frameworks von React anschauen. Das sollten wir eher ergänzend zu unseren Ideen nutzen
- Das folgende hab ich notiert aber weiß nichtmehr was ich damit gemeint habe: Herkunft der Daten: Würde sehr gut passen. Data Mesh anschauen, da geht es auch darum dass man die Herkunft der Daten kennt.
- Es muss Möglichkeiten geben, die Daten zu bereinigen. Es wäre cool wenn es eine Art Transform-Einheit gäbe, aber das müssten wir nicht unbedingt selbst implementieren, sondern kann auch Mock-Mäßig eingebunden sein. Es kommt darauf an wie wir die Schwerpunkte setzen. 

## Was Kirenz noch von uns Wissen möchte

- Er würde würde Workshops zu Schwerpunktthemen geben, da müssen wir ihm sagen wo wir noch Unterstützung/Input brauchen
- Bis zum Termin am 6. Oktober sollte man sich auf einen konkreten Vorschlag eines Use Cases festlegen. 
- Man soll festlegen was die Schwerpunkte sind und wer sich innerhalb der Gruppe mit was beschäftigt (trotzdem soll sich jeder in der Gruppe mit dem Gesamtsystem auskennen). Das ist hauptsächlich für die Bewertung für ihn geschickt. 

## Besprechung der Gruppe

- Die Gruppe trifft sich am 4. Oktober abends nochmal zwecks möglicher Themen etc. Bis dahin sollte jeder einen groben Plan haben in welche Richtung es gehen soll. 
