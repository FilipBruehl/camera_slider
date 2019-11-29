# Server

---

## Server Programm des Camera-Slider Projektes

---

### Voraussetzungen

* Python 3.7.x
  * python-socketio
  * gphoto2
* gphoto2
* libgphoto2-dev

Zum Installieren von *gphoto2* und *libgphoto2-dev* muss folgender Befehl in der Kommandozeile des Pis eingegeben werden:

```bash
sudo apt-get install gphoto2 libgphoto2-dev
```

Zum Installieren der notwendingen Python-Bibliotheken muss in der Kommandozeile des Pis folgender Befehl ausgeführt werden:

```bash
sudo pip install -r requirements.txt
```

---

### Benutzung

Zum Starten des Servers muss in der Kommandozeile des Pis folgender Befehl ausgeführt werden:

```python
python main.py
```
