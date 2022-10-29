# geschichte-viz

## Verweise

Zeigt die Querverweise zwischen Episoden in einem gerichteten Graph.

### Plan:

- Die Referenzen in [einer Datei](data/references.toml) erfassen
- RSS-Feed parsen als Datengrundlage
- Mergen der Daten von Feed und references.toml
- Transformation in einen Graph, speichern als JSON
- Renderering des Graphen mit [Cyptoscape](https://cytoscape.org)
