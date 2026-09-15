# Python GUI Apps

Small desktop GUI programs built with PySimpleGUI (which runs on top of tkinter), plus two one-off SQLite scripts. They were written while learning forms, event loops, popups, modal second windows, date pickers and database schema changes: a flight reservation form (with and without a reservations list), a kilometers-to-miles converter, a sphere-volume and circle-area calculator, PySimpleGUI's all-elements demo, and the helper scripts for an elder-care app.

> The elder-care / caregiver app from the same period has its own repository: **[Seniory](https://github.com/joserico00/Seniory)**. `submitData.py` and `Aaltertable.py` in this project are pieces related to that app.

## Contents

| File | What it is | Status |
|---|---|---|
| [`airportreservation.py`](#airportreservationpy) | Flight reservation form that shows a confirmation popup | Runs |
| [`flighreservepop.py`](#flighreservepoppy) | Same form, plus an in-memory reservations list in a modal window | **Syntax error** (stray `def`) |
| [`kilometertometerconver.py`](#kilometertometerconverpy) | Kilometers-to-**miles** converter | Runs |
| [`multiplewindows.py`](#multiplewindowspy) | Sphere volume calculator that opens a second circle-area window | Runs |
| [`guitest.py`](#guitestpy) | First PySimpleGUI form: collect names | Runs |
| [`pythonsampledemo.py`](#pythonsampledemopy) | PySimpleGUI's "all elements" demo program (third-party, for reference) | Runs |
| [`submitData.py`](#submitdatapy) | Menu window for submitting elder / caregiver records | Needs modules from the elder-care app |
| [`sqltst.py`](#sqltstpy) | Creates a test SQLite table | Runs once |
| [`Aaltertable.py`](#aaltertablepy) | Adds a `HELP` column to the elder-care `ELDERS` table | Needs an existing `central.db` |

### SQLite usage at a glance

| Database file | Table | Statement | Script |
|---|---|---|---|
| `testda.db` | `DATAATBLE (FIRSTINDEX TEXT NOT NULL, SECONDINDEX INT)` | `CREATE TABLE` | `sqltst.py` |
| `central.db` | `ELDERS` (existing) gets a new column, `HELP TEXT` | `ALTER TABLE ELDERS ADD COLUMN HELP TEXT` | `Aaltertable.py` |

None of the scripts insert or query rows. The reservation apps keep everything in memory and do not use a database.

---

## `airportreservation.py`

A single-window flight booking form. Window title: `привет Airlines`. Theme: `Black`.

| Element | Key | Purpose |
|---|---|---|
| Text input | `-NAME-` | Full name |
| Text input | `-PASSPORT_NUMBER-` | Passport number |
| Radio buttons (group `"RADIO"`) | `-MALE-`, `-FEMALE-` | Gender; only one can be selected |
| Input + `CalendarButton("DATE OF DEPARTURE")` | `-DEPARTURE-` | A date picker fills in the input |
| Input + `CalendarButton("DATE OF ARRIVAL")` | `-ARRIVAL-` | A date picker fills in the input |
| Listbox (single selection) | `-DESTINATION-` | Havana, Moscow, Beijing, Tehran, Damascus, Tripoli, Sanaa |
| Buttons | none | `Reserve Ticket`, `See Reservations`, `Exit` |

**Flow**
1. The event loop reads `(event, values)` from the window.
2. **Reserve Ticket** calls `format_input_information(values)`, which builds a multi-line summary (`Flight booked!`, Name, Passport Number, Gender, Departure Time, Arrival Time, Destination) and shows it with `sg.popup`.
3. Gender is `Female` if that radio button is selected and `Male` otherwise, including when neither is selected.
4. **Exit** or closing the window ends the loop.

**Notes**
- **See Reservations** has no handler in this version; `flighreservepop.py` adds one.
- Nothing is saved.
- Clicking **Reserve Ticket** without choosing a destination raises `IndexError` (`values['-DESTINATION-'][0]` on an empty list), which closes the app.

## `flighreservepop.py`

A second version of the reservation form that stores bookings and lists them in a popup window.

**What it adds to `airportreservation.py`**
- `reservations_array`: a list of bookings kept in memory.
- `format_input_information(values)` returns a single-line string (` , Name: … , Passport Number: … , Gender: … , Departure Time: … , Arrival Time: … , Destination: …`) that fits in one listbox row.
- `store_information_in_array(values, reservations_array)` adds the current booking to the list.
- `reservations_window(reservations_array)` opens a **modal** window titled "Reservations Window", with a listbox of every stored reservation and an `Exit` button. The layout is built inside the function because PySimpleGUI cannot reuse a layout for a second window.
- The main window is fixed at 300×300. **Reserve Ticket** stores the booking and shows the popup; **See Reservations** opens the modal list.
- Comments at the top list planned next steps (multiple windows, multiple files, a QR-code tutorial).

**Status:** does not run. Line 64 contains a lone `def` before the event loop, which is a `SyntaxError`. Apart from that line, the logic is complete.

## `kilometertometerconver.py`

Despite the file name, this converts **kilometers to miles** (factor `0.6214`), not meters.

| Element | Key | Purpose |
|---|---|---|
| Text input ("Enter distance in Kilometers") | `-KILO-` | Distance in km. `do_not_clear=False` empties it after every event. |
| Text output | `-OUT-KM-` | Shows the km value that was entered |
| Text output | `-OUT-MI-` | Shows `float(km) * 0.6214` |
| Buttons | none | `Convert` (also triggered by Enter via `bind_return_key=True`), `Quit` |

Every event other than Quit or closing the window updates both outputs. The theme is set with the older `sg.change_look_and_feel('GreenTan')` call.

**Notes**
- An empty or non-numeric input raises `ValueError` and closes the app.
- The result is not rounded (for example, `3` km gives `1.8641999999999999`), so long values may be clipped by the 5-character output field.

## `multiplewindows.py`

Two geometry calculators that show how to open a second (modal) window. Theme: `DarkAmber`.

- **Main window, "Calculate Sphere Volume"** (500×100): a radius input `-RADIUS-` in centimeters, an output `-OUT-CALCULATION-` labeled "centimeters cubed", and the buttons `Calculate Volume`, `Calculate Area` and `Quit`.
  - **Calculate Volume** computes V = 4/3·π·r³ with `math.pi`.
  - **Calculate Area** calls `calculate_area_window()`.
- **Modal window, "Calculate Circle Area"**: its own radius input and a `Calculate Area` button that computes A = π·r² into `-OUT-AREA-CALCULATION-` ("centimeters squared"). **Quit** closes it and returns to the main window. Like the reservation list, its layout is built inside the function so a fresh window can be created each time.

**Notes:** an empty or non-numeric radius raises `ValueError`.

## `guitest.py`

A first PySimpleGUI test. It prints the imported module object, then opens a window titled "Form" with an "Enter name" label, an `InputText` element (automatic key `0`), and `Ok` and `Cancel` buttons.

- Every event except **Cancel** prints `values[0]` and appends it to `list_of_names`.
- **Cancel** ends the loop and prints the list.

**Notes:** closing the window with the title-bar button returns `values = None`, so `values[0]` raises `TypeError`. Use **Cancel** to exit.

## `pythonsampledemo.py`

**Not the author's own work.** This is a demo program from the PySimpleGUI project (its official "Demo of (almost) all Elements" program), included only as a reference for the elements used in the other scripts. Its header carries the PySimpleGUI copyright.

`make_window(theme)` builds a resizable window with a custom title bar. It stays on top of other windows, can be dragged from anywhere, and has a size grip. The window contains:

- A custom menu bar: **Application → Exit**, **Help → About**.
- A window-wide right-click menu: `Edit Me`, `Versions`, `Nothing`, `More Nothing`, `Exit`.
- A `TabGroup` with six tabs:
  - **Input Elements:** Input, Slider, animated loading GIF, Checkbox, two Radio buttons, Combo, OptionMenu, Spin, Multiline, a `Button`, a `Popup` button and an image button.
  - **Asthetic Elements:** Image and a ProgressBar with a `Test Progress bar` button.
  - **Graphing:** a 200×200 `Graph` (click to draw a yellow circle; it has its own right-click menu) and a two-row `Table` with Name and Score columns.
  - **Popups:** `Open Folder` and `Open File` buttons, which use `popup_get_folder` and `popup_get_file`.
  - **Theming:** a listbox of every built-in theme and a `Set Theme` button that closes and rebuilds the window with the chosen theme.
  - **Output:** a Multiline that captures `stdout` and `stderr`.

`main()` reads events with `window.read(timeout=100)`, advances the GIF animation on every pass, and prints each event with its values dictionary, which shows up in the Output tab. It also handles About, Popup, the progress bar, graph clicks, the folder and file choosers, theme changes, **Edit Me** (`sg.execute_editor(__file__)`) and **Versions** (`sg.get_versions()`). The `__main__` block sets the theme three times in a row, so `dark green 7` is the one used.

## `submitData.py`

A menu window for the elder-care app. `Submitpage()` opens a resizable window titled "Sumbit data" (spelled that way in the code) with the heading "Submiting into the databases", in a large `Any 50` font, and two buttons:

| Button | Action |
|---|---|
| `Submit Elder` | `eldergui.ElderSubmit()` |
| `Submit Caregiver` | `caregivergui.CaregiverSubmit()` |

**Notes**
- `eldergui` and `caregivergui` are **not in this project**; they belong to the elder-care app ([Seniory](https://github.com/joserico00/Seniory)). Without them the imports raise `ModuleNotFoundError`.
- The call to `Submitpage()` at the bottom is commented out, so the file is meant to be imported rather than run directly.
- `sqlite3` is imported but not used.

## `sqltst.py`

A minimal SQLite test:

```sql
CREATE TABLE DATAATBLE
  (FIRSTINDEX  TEXT NOT NULL,
   SECONDINDEX INT);
```

It connects to `testda.db` in the current directory (creating the file if needed), runs the statement and closes the connection. There is no `commit()`, but Python's `sqlite3` module runs `CREATE TABLE` outside an implicit transaction, so the table is saved anyway. Running the script a second time raises `sqlite3.OperationalError: table DATAATBLE already exists`. No rows are inserted.

## `Aaltertable.py`

A one-statement schema change for the elder-care database:

```sql
ALTER TABLE ELDERS ADD COLUMN HELP TEXT
```

It connects to `central.db`, runs the statement, commits and closes. It expects `central.db` to already contain an `ELDERS` table, created by the elder-care app. If the file is missing, `sqlite3.connect` creates an empty `central.db` and the statement fails with `no such table: ELDERS`. Running it twice fails with `duplicate column name: HELP`.

---

## Requirements

- Python 3.7+ with **tkinter**. The python.org installers include it; with Homebrew on macOS, run `brew install python-tk`.
- **PySimpleGUI 4.x.** The scripts use the 4.x API (`CalendarButton`, `change_look_and_feel`, `MenubarCustom`, `Sizegrip`, among others), and `pythonsampledemo.py` needs a recent 4.x release.
  - PySimpleGUI changed its licensing and distribution with version 5. If a 4.x release isn't available to you, **FreeSimpleGUI** is a community fork of the LGPL 4.x code with the same API. It is imported under a different module name, so the `import` lines would need to change.
- `sqlite3` (standard library) for the database scripts. The `sqlite3` command-line tool is optional, for inspecting the files.

```bash
pip install PySimpleGUI     # or: pip install FreeSimpleGUI
```

## Usage

Each GUI script opens its own window:

```bash
python3 airportreservation.py
python3 kilometertometerconver.py   # type 10, press Enter -> 10 * 0.6214 ≈ 6.214 miles
python3 multiplewindows.py          # radius 2 -> volume 33.51...; "Calculate Area" opens the second window
python3 guitest.py                  # use Cancel to exit
python3 pythonsampledemo.py
```

Database scripts (run them from the folder where the `.db` file should be):

```bash
python3 sqltst.py                   # creates ./testda.db with table DATAATBLE
sqlite3 testda.db ".schema"

python3 Aaltertable.py              # requires ./central.db with an ELDERS table
```

## Author

Jose E. Rodriguez Rios
