# fan-monitor
Remotely monitors building ventilation fans via The Things Network(TTN) LoRaWAN. In many instances the fan status can only be found by observing lamps on a panel that are located in a Plant Room. This project allows instant notification of a fan being turned off or failing.

## System Overview
![System Overview](https://github.com/roscoe81/fan-monitor/blob/main/Documentation/Northcliff%20Fan%20Monitor%20Overview%20Gen.png).

This monitor allows [Home Manager](https://github.com/roscoe81/Home-Manager) (>= Version 9.28) to remotely capture the fan status over LoRaWAN via The Things Network and provide notifications via Apple HomeKit or Pushover.

## Hardware
![Fan Status Lamp Interface](https://github.com/roscoe81/fan-monitor/blob/main/Documentation/Fan%20Monitor%20Interface_schem.png)
This circuity provides an interface between the 24VAC fan run and fault lamps and the Pycom lopy4 microcontroller. That microcontroller runs the [Micro Python code](https://github.com/roscoe81/fan-monitor/blob/main/northcliff_fan_monitor_Gen.py) to convert the status of each lamp to LoRaWAN payloads that are sent to Home Manager via The Things Network.

**This project should only be constructed and deployed by a licenced electrician. See LICENCE.md for disclaimers.**

## Operation
The system can sense the following fan states:

1. Exhaust Fan Fault

2. Exhaust Fan Run

3. Outside Fan Fault

4. Outside Fan Run

5. Garage Fan Fault

6. Garage Fan Run

The fan [states](https://github.com/roscoe81/fan-monitor/blob/main/Photos/image1.png) and [alerts](https://github.com/roscoe81/fan-monitor/blob/main/Photos/image2.png) can be monitored the Apple Home App via [Home Manager](https://github.com/roscoe81/Home-Manager). Notifications can also be provided via [Pushover](https://github.com/roscoe81/fan-monitor/blob/main/Photos/image3.png).

## License
This project is licensed under the MIT License - see the LICENSE.md file for details




