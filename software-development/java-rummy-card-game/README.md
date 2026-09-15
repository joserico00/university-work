# Java Rummy Card Game

A two-player desktop card game developed as university coursework with Java Swing. Players draw from the deck or discard pile, discard cards, and lay matching-rank sets on the table.

## Features

- A shuffled 52-card deck and discard pile
- Separate hands and controls for two local players
- Set validation and table placement by rank
- Custom deck, hand, set, and stack data structures
- Swing panels for hands, card piles, and completed sets

## Build and run

Run the commands from this directory with JDK 8 or newer:

```powershell
New-Item -ItemType Directory -Force out
javac -d out src\*.java
java -cp out RummyGame
```

The program loads card images from the `cards/` directory, so keep that directory beside `src/` and `out/` when running the game.

## Attribution and license

This is an adapted course project, not a claim of sole authorship over the supplied framework.

- Jose E. Rodriguez Rios implemented and extended the game-specific behavior in the submitted coursework.
- `Card.java` credits John K. Estell and Patti Ordonez in its original header.
- `Table.java` credits Patti Ordonez as the GUI framework author.
- The playing-card artwork and supporting framework were supplied with the course materials.

The original notices remain in the source files. The included `COPYING` file contains the GNU General Public License version 2 that accompanied the project. Redistributed and modified versions must follow those terms.

## Current state

The source has been reorganized for GitHub, compiled artifacts and Eclipse metadata were removed, resource paths were made explicit, and the entry point was renamed to `RummyGame`. The Swing code still reflects the style and limitations of the original coursework.
