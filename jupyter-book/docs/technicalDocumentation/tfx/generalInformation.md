# General information about TFX

[Understanding TFX Pipelines &nbsp;|&nbsp; TensorFlow](https://www.tensorflow.org/tfx/guide/understanding_tfx_pipelines)

## Artefakte

Aufgabe nach jedem Schritt in einer tfx-pipeline wird als Artefakt bezeichnet. Nachfolgende Schritte können die Artefakte dann als Eingabe verwenden. So können Daten zwischen den einzelnen Schritten in der Pipeline übetragen werden. 

z.B. Example Gen --> Statistic Gen

## ML-Metadaten

In jedem Lauf werden Metadtan erzeugt. Vergleichbar mit einem Logfile in der Softwareentwicklung. Fehler, unterwartetes Verhalten etc. wird hierin protokolliert. 

MLMD hilft Ihnen, alle miteinander verbundenen Teile Ihrer ML-Pipeline zu verstehen und zu analysieren, anstatt sie isoliert zu analysieren, und kann Ihnen helfen, Fragen zu Ihrer ML-Pipeline zu beantworten, wie zum Beispiel:

- Auf welchem ​​Datensatz wurde das Modell trainiert?
- Welche Hyperparameter wurden zum Trainieren des Modells verwendet?
- Welcher Pipelinelauf hat das Modell erstellt?
- Welcher Trainingslauf führte zu diesem Modell?
- Welche Version von TensorFlow hat dieses Modell erstellt?
- Wann wurde das gescheiterte Modell gepusht?

[ML Metadata &nbsp;|&nbsp; TFX &nbsp;|&nbsp; TensorFlow](https://www.tensorflow.org/tfx/guide/mlmd#concepts)

## Parameter

Parameter sind Eingaben in Pipelines die vor der Ausführung bekannt sind. 

Parameter können Verhalten der Pipeline verändern ohne das man Code anpassen muss. Sie können beispielsweise Parameter verwenden, um eine Pipeline mit verschiedenen Hyperparametersätzen auszuführen, ohne den Code der Pipeline zu ändern.

## Komponente

## Pipeline

= tragbare Implementierung eines ML-Worklfows. Kann auf verschiedenen Orchestratoren wie z.B. Apache Airflow, Kubeflow ausgeührt werden.

Basierend auf dieser Analyse führt ein Orchestrator Folgendes aus:

- Die Datenaufnahme-, StatisticsGen- und SchemaGen-Komponenteninstanzen werden nacheinander ausgeführt.
- Die Komponenten ExampleValidator und Transform können parallel ausgeführt werden, da sie Abhängigkeiten von Eingabeartefakten gemeinsam haben und nicht von der Ausgabe des anderen abhängen.
- Nach Abschluss der Transformationskomponente werden die Instanzen der Trainer-, Evaluator- und benutzerdefinierten Deployer-Komponenten nacheinander ausgeführt.
