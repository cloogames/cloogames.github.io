# games

A few browser games, hosted on GitHub Pages. Every game is a self-contained
HTML file with no build step and no dependencies beyond a webfont.

## Layout

    index.html               the hub
    guess-who/index.html     the game
    guess-who/boards/        board rosters, loaded on first visit
    guess-who/photo-sets/    optional photo URLs, pasted in by hand
    guess-who-preview.html   generated single file, boards baked in
    .nojekyll                serve files as-is, no Jekyll processing

## Boards

The game ships with no roster of its own. On a visitor's first load it reads
`guess-who/boards/index.json` and pulls in every board listed there:

    [
      {"name": "Disney Channel", "file": "disney-channel.json"},
      {"name": "F1 2026",        "file": "f1-2026.json"},
      {"name": "Studio Ghibli",  "file": "studio-ghibli.json"},
      {"name": "Pixar",          "file": "pixar.json"},
      {"name": "Nintendo",       "file": "nintendo.json"}
    ]

Each board file is a plain array, the same shape the in-game paste box takes:

    [
      {"name": "Raven Baxter", "show": "That's So Raven"},
      {"name": "Lando Norris", "show": "McLaren"}
    ]

`show` is optional. It tints the placeholder card and prints under the name.

Add a board by dropping a `.json` file in `boards/` and adding a line to
`index.json`. Boards are copied into the browser on first load, so edits and
photos stay local to whoever is playing and changing a file here won't
overwrite them. Use "Import from boards/" in the edit bar to pull in new ones.

Note that reading the folder needs the page served over http. Opened straight
off disk the game starts empty and tells you so; paste a theme in by hand.

## Photo sets

`boards/` stays names only, on purpose. `photo-sets/` holds the same rosters
with an `img` URL on each card, which the game is not wired to read. Paste one
into "Paste a theme" to load a whole board of pictures at once.

Cards loaded this way are *linked*, not copied, and carry an amber dot. They
need the network every time the page loads. To make one permanent, drag the
image file onto the card instead, which bakes it into local storage.

Only `f1-2026.json` has a set. Those are real people with Creative Commons
photos on Wikimedia Commons. The other four boards are copyrighted characters
with no free image source, so their pictures have to be supplied by hand.

## Serving it locally

    python3 -m http.server        # inside the repo root, then localhost:8000

There is no Python on the Windows box this was last worked on. Any static
server does; the point is only that it be http and not `file://`.

## Adding a game

1. Drop the game in its own folder with an `index.html` inside.
2. Add an entry to the `GAMES` array at the bottom of `index.html`.

Keep paths relative, with no leading slash, so the site works at whatever
address it's served from.

## Publishing

Settings > Pages > Deploy from a branch > `main` / root.

By default this serves at `<username>.github.io/<repo>/`. To give it its own
address instead, add a `CNAME` file containing a single line with the host
(for example `games.example.com`) and point a DNS CNAME record at
`<username>.github.io`.
