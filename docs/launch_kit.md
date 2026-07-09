# Launch Kit

Use this page when announcing Weather Station Core, submitting it to directories,
or making demo assets. The goal is simple: show one useful outcome first, then
let the depth support it.

---

## Main pitch

**Weather Station Core tells Home Assistant when rain is about to start, using
your own weather station as ground truth.**

Short version:

> Turn any Home Assistant weather station into actionable local weather
> automation: rain countdowns, ET0 irrigation, fire danger, heat stress,
> dashboards, blueprints, 50+ fully local core sensors, and 170+ derived sensors
> with optional feature packs.

---

## 10-second GIF recipe

Create this once and reuse it everywhere.

1. Enable **Precipitation Nowcast**.
2. Put these entities on a small dashboard view:
   - `sensor.ws_minutes_until_rain`
   - `sensor.ws_rain_rate`
   - `sensor.ws_rain_probability_combined`
   - the Rain Start Warning automation trace or notification.
3. Record a 10-second clip:
   - first frame: "Rain expected in 7 min"
   - middle: notification appears
   - final: rain rate begins rising or the countdown reaches 0.
4. Export as `screenshots/rain-countdown-demo.gif`.
5. Add it near the top of `README.md`, above the dashboard screenshot.

If live rain is inconvenient, create a temporary demo dashboard using entity
states from Developer Tools. Do not commit fake sensors or demo helpers.

---

## Home Assistant Community draft

Title:

```text
Weather Station Core: know when rain starts from your own weather station
```

Post:

```markdown
I built a custom integration for people who already have a personal weather
station in Home Assistant and want the data to become useful automations instead
of just dashboard numbers.

The headline feature is a rain countdown:

`sensor.ws_minutes_until_rain`

When Precipitation Nowcast is enabled, ws_core blends your local rain gauge with
Open-Meteo's 15-minute forecast grid, so Home Assistant can warn before the first
drop. It works with any station already exposed as HA entities: Ecowitt,
WeatherFlow Tempest, Ambient Weather, Davis, Netatmo, MQTT sensors, etc.

What it adds:

- 50+ fully local core derived sensors
- 170+ derived sensors with optional feature packs
- ET0 irrigation sensors
- FWI / FFDI / FFWI fire danger
- UTCI / WBGT heat stress
- air quality, pollen, lightning, soil, indoor, diagnostics
- drop-in dashboards
- 10 ready-to-use blueprints
- 8 translations

Install:

https://github.com/kmich/ha_ws_core

One-click HACS custom repository:

https://my.home-assistant.io/redirect/hacs_repository/?owner=kmich&repository=ha_ws_core&category=integration

I would especially love feedback from users with Ecowitt WS90, WeatherFlow
Tempest, Ambient Weather, Davis, Netatmo, and local MQTT stations.

If you try it, tell me:

1. which station you use,
2. whether auto-discovery found the right sensors,
3. which automation you built first.
```

First reply to reserve:

```markdown
Useful starting points:

- Rain alerts: Rain Start Warning blueprint
- Irrigation: ET0 + Irrigation Rain Skip blueprint
- Awnings/blinds: High Wind Gusts blueprint
- Frost: Freeze Warning blueprint
- AQI: Poor Air Quality blueprint

Docs: https://kmich.github.io/ha_ws_core/
```

---

## Reddit draft

Title:

```text
I got tired of my weather station not telling me when rain would actually start, so I built this
```

Body:

```markdown
I have a personal weather station in Home Assistant, but most of the data just
sat there as dashboard numbers. I wanted it to answer practical questions:

- when will rain start?
- should irrigation run today?
- should the awning retract?
- is today dangerous for heat stress or fire weather?

So I built Weather Station Core. It reads the weather station entities already
in HA and creates derived sensors, dashboards, and blueprints.

The most useful sensor so far is:

`sensor.ws_minutes_until_rain`

It uses your local rain gauge plus nowcast data to warn before rain starts.

Repo: https://github.com/kmich/ha_ws_core

I am looking for testers with Ecowitt, WeatherFlow Tempest, Ambient Weather,
Davis, Netatmo, and MQTT-based stations. If you try it, I would love to know
which station you use and whether the setup wizard maps your entities cleanly.
```

---

## GitHub repository metadata

Suggested **About** description:

```text
Know when rain starts from your own Home Assistant weather station. 170+ derived sensors, ET0 irrigation, fire danger, UTCI heat stress, dashboards, and blueprints.
```

Suggested topics:

```text
home-assistant
home-assistant-custom-component
hacs
weather
weather-station
personal-weather-station
ecowitt
weatherflow
ambient-weather
davis-weatherlink
netatmo
irrigation
evapotranspiration
nowcasting
zambretti
fire-weather-index
utci
lightning-detection
```

---

## Directory submissions

### HACS default repository

Use the HACS default repository process. Before submitting, confirm:

- repository is public,
- GitHub About description is outcome-focused,
- topics include `home-assistant`, `hacs`, `weather-station`, and station names,
- `hacs.json` exists in the root,
- GitHub releases are published,
- README has installation, usage, and screenshots.

### Awesome Home Assistant

Open a pull request to:

```text
https://github.com/frenck/awesome-home-assistant
```

Suggested entry:

```markdown
- [Weather Station Core](https://github.com/kmich/ha_ws_core) - Turn any Home
  Assistant weather station into rain countdowns, ET0 irrigation, fire danger,
  heat stress, dashboards, blueprints, and 170+ derived sensors.
```

### Best-of / ranked lists

Submit after the next GitHub release is visible and the README has the GIF.
These lists favor projects that already have a clear screenshot, tags, releases,
and a crisp one-line description.
