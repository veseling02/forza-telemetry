# Forza Live Telemetry

A real-time telemetry dashboard for Forza Horizon, written in Python with pygame. The game streams its telemetry over UDP; this app catches the packets, decodes them, and draws what your hands and the car are doing — live, at 60 fps.


## What it shows

- **Gas and brake traces** — the last 4 seconds of throttle and brake input, drawn as scrolling line graphs. Great for spotting whether you're actually smooth on the pedals or just think you are (I was not).
- **RPM panel** — a bar that fills with revs, with the current RPM on a fixed plate. Near redline it flashes red/orange as a shift light.
- **Speed readout** — current speed in km/h.
- **Steering wheel** — a wheel that rotates up to 540° like the in-game animation, with a marker stripe so you can track it mid-turn. The raw controller input snaps around instantly, so the display runs it through a small exponential filter to make it move like a real wheel.

## How it works

Forza can broadcast its telemetry over UDP — a ~324-byte packet, 60 times a second, with every value sitting at a fixed byte offset. `harvester.py` listens on a background thread, pulls out the values I care about with `struct.unpack`, and normalizes them on the spot (gas and brake as 0–1, steering clamped to ±1) so the rest of the app never touches raw bytes. Throttle and brake go into fixed-length deques holding the last 4 seconds for the traces; single values like RPM, speed, and steering just overwrite a `latest` dict.

`main.py` reads from those and redraws at 60 fps with pygame. No panel position is hardcoded — every rect is placed relative to its neighbor, so changing one panel reflows the rest. Steering gets a small exponential filter at display time only; the stored value stays raw, so anything that consumes it later gets the truth.

One deliberate choice: if the socket can't bind at startup (port taken, second instance running), the app crashes immediately instead of starting anyway. A dashboard quietly drawing zeros is worse than no dashboard.

## Running it

You'll need Python 3 and pygame:

```
pip install pygame
python main.py
```

Then tell Forza to send telemetry. In game: **Settings → HUD and Gameplay → Data Out**, set it to ON with IP `127.0.0.1` and port `6969`. The app listens on localhost only, so Windows won't ask for firewall permission; if your game runs on a console or another PC, change `UDP_IP` to `"0.0.0.0"` in `harvester.py` (and expect the firewall prompt — that's it doing its job). Built and tested against the Forza Horizon packet layout; Motorsport uses different offsets and won't decode correctly.

To build a standalone Windows exe:

```
pip install pyinstaller
pyinstaller --onefile --noconsole --name ForzaTelemetry main.py
```

The finished `ForzaTelemetry.exe` lands in `dist/` and runs without Python installed.

## What I learned building this

I went in thinking the hard part would be reading the UDP packets. It wasn't — that's ten lines of `struct.unpack` once you know the offsets. The hard parts were everywhere else.

My first version created the socket inside the background thread, so when the port was already taken the thread just died on its own and the app kept running, drawing flat lines forever. I debugged the drawing code for a while before realizing nothing was ever arriving. Moving the bind to startup so it fails loudly taught me more about threads than any tutorial had.

Graphics coordinates took some getting used to — y grows downward, so drawing a value going "up" means subtracting. At one point my traces rendered completely sideways because I'd paired the coordinates wrong, (x1, x2) instead of (x1, y1). And the steering wheel was the first time the unit circle from school felt like something I actually needed.

The lesson I keep coming back to, though, is about motion: the number plates originally resized themselves to fit each value, and the whole dash felt busy for no reason. Making them fixed-size, sized for the worst case, calmed everything down. Movement on a dashboard should mean something.

## Ideas for later

- A "NO SIGNAL" state when packets stop arriving, instead of frozen zeros
- Gear indicator (it's one byte in the packet)
- Grip meter driven by tire slip angles
