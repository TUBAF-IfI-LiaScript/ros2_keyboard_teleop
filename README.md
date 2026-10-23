# ros2_keyboard_teleop

_Idee: Johannes Kohl · Autoren: Sebastian Zug & Claude Code (Opus 5.5) · TU Bergakademie Freiberg_

Ein kleines Paketbündel zur Tastatursteuerung für ROS 2 Jazzy – geschrieben für die Übung **Ü 2 „Ihr erster Workspace“** der Veranstaltung Robotik. Es zeigt, wie man Pakete anderer Leute in den eigenen Workspace holt, und wie sich C++- und Python-Pakete und ein reines Bündelpaket unterscheiden.

| Paket | Bauart | Inhalt |
| :-- | :-- | :-- |
| `keyboard_teleop_cpp` | `ament_cmake` (C++) | Knoten `keyboard_input`: liest Tasten und veröffentlicht `/keyboard_teleop/linear` und `/keyboard_teleop/angular` (`std_msgs/msg/Float64`, 10 Hz) |
| `keyboard_teleop_viz` | `ament_python` | Knoten `anzeige`: zeigt die aktuelle Vorgabe als Balken an |
| `keyboard_teleop` | `ament_cmake`, ohne Code | bündelt beide Pakete (`exec_depend`) und startet die Anzeige mit `anzeige.launch.py` |

Einen Fahrbefehl (`geometry_msgs/msg/Twist` auf `cmd_vel`) erzeugt das Bündel bewusst **nicht** – das ist die Aufgabe der Studierenden.

## Bauen und starten

```bash
cd ~/ros2_ws/src
git clone https://github.com/IfI-TUBAF-Robotik-2026/ros2_keyboard_teleop.git
cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash

ros2 run keyboard_teleop_cpp keyboard_input        # eigenes Terminal: w/s schneller/langsamer, a/d drehen, Leertaste Stopp, q Ende
ros2 launch keyboard_teleop anzeige.launch.py      # zweites Terminal
```

`keyboard_input` braucht die Tastatur seines eigenen Terminals und wird deshalb mit `ros2 run` gestartet, nicht aus einer Launch-Datei.

## Vorlagen für Ü 2

Der Ordner `vorlagen_ue2/` enthält die Dateien, die in Ü 2 in das eigene Paket `mein_teleop` kopiert werden: `umsetzer.py` (mit zwei TODO), `launch/teleop.launch.py` und `config/umsetzer.yaml`. Die Datei `COLCON_IGNORE` verhindert, dass `colcon` den Ordner baut.

## Parameter

| Knoten | Parameter | Standard |
| :-- | :-- | :-- |
| `keyboard_input` | `step_linear`, `step_angular` | 0,05 m/s, 0,25 rad/s je Tastendruck |
| | `max_linear`, `max_angular` | 0,5 m/s, 2,0 rad/s |
| | `rate` | 10 Hz |
| `keyboard_viz` | `max_linear`, `max_angular` | Skalierung der Balken |

## Lizenz

BSD-3-Clause
