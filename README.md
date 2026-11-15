# Panta Rhei — Ecosistema Simulado

Proyecto final de **MO-0002 Programación I** (UCR, Sede de Occidente, II Ciclo 2026).
Una cuadrícula del bosque tropical seco de Guanacaste donde plantas, guatusas
(herbívoros) y tigrillos (carnívoros) nacen, se mueven, comen, se reproducen y
mueren por turnos. La partida termina cuando una especie se extingue.

## Cómo correrlo

```bash
pip install -r requirements.txt
python main.py                       # ventana con una partida nueva
python main.py --semilla 42          # partida repetible
python main.py --consola 10          # 10 turnos por consola
```

## Pruebas

```bash
python -m unittest discover -s pruebas -t .
```

## Documentación

Propuesta, diagrama de clases y decisiones de diseño están en la carpeta `docs/`.
