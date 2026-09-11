# Guess Who

A browser Guess Who board for two people playing over a voice call. Part of a
small games site that is deliberately unrelated to markusclipper.com.

Questions are asked out loud, so the app does not track them. It is an
elimination board and nothing more: click a card to knock it out, click again
to bring it back. There is no turn logic, no scoring, no win condition, and no
opponent. Do not add any.

## Hard constraints

- **No build step, no dependencies, no framework.** Each game is one HTML file
  with inline CSS and JS. The only external request is a Google Fonts link,
  which degrades to system fonts. Keep it that way.
- **No browser storage beyond `localStorage`.** Boards and photos live there.
- **All paths relative, never leading-slash.** The site must work unchanged at
  `user.github.io/repo/`, at a bare custom domain, and at `localhost`.
- **Never commit photos of real people into `boards/`.** Rosters are names
  only. Photos are added by the user at play time.

## Decisions that should not be quietly reversed

- **Elimination is fade, not flip.** An earlier version rotated cards face
  down. It was replaced on purpose.
- **Knocked-out cards must keep a readable name.** Fading the whole card
  toward a light page drops the nameplate to ~2:1 contrast. The current
  approach removes the shadow and dulls the fill instead, holding ~4:1.
- **The blur is on an overlay, not the photo.** `backdrop-filter` on
  `.portrait::after`. Blurring the image directly forced a 7% upscale to hide
  soft edges, which re-cropped every face. There is an `@supports` fallback.
- **The game ships with no roster of its own.** Boards are JSON in
  `guess-who/boards/`, listed in `index.json`. Do not reintroduce a hardcoded
  default roster.
- **A `show` field is cosmetic only.** It tints the empty-photo card and prints
  under the name. It drives no logic.
- **Boards shuffle when created, never on render.** The source files are
  grouped by show or team, which would otherwise put all teammates adjacent.
  Reordering mid-game would break card positions.

## Gotchas, all of which have bitten

- **`fetch` fails on `file://`.** Opening the game by double-click cannot read
  `boards/`. It shows an empty board explaining this. Serve over http to work
  on it: `python3 -m http.server` inside `guess-who/`.
- **`localStorage` and `history.replaceState` throw on a null origin.** Every
  access goes through `safeGet`/`safeSet`. Do not call them directly.
- **Stored boards used to win unconditionally over starter boards**, so one
  empty saved board made the app look permanently broken. `loadAll()` now
  filters out boards with no cards. Keep that filter.
- **Photos dragged from a browser tab arrive as a URL, not bytes.** The drop
  handler reads `text/html` and `text/uri-list`. If the host allows
  cross-origin reads the pixels are baked to a data URL; otherwise the canvas
  taints, and only a link can be stored. Linked cards show an amber dot.
- **`localStorage` caps around 5MB**, which is roughly five to ten boards of
  baked photos. A board that fails to save is rolled back rather than left on
  screen to vanish on reload.
- **Test against dirty state, not just a clean load.** Most bugs here came
  from stale `localStorage`, and a clean-boot test passed every time.

## Visual language

Four colours, defined at the top of each file. Resist adding a fifth.

    --page   #FBF7F2   warm off-white, the background
    --card   #FFFFFF   cards, panels, dialogs
    --ink    #4A352F   deep umber, all text
    --accent #9E472A   muted rust: primary button, focus rings, your own card
    --sand   #D9B99B   only appears on a card with no photo yet

White on off-white is 1.07:1, so cards are separated by a hairline in the
shadow stack. Do not "fix" this by darkening the page.

Type is Fraunces for display and Archivo for UI.

Check contrast numerically when changing colours. A warm low-contrast palette
is exactly where text quietly stops being readable. Target 4.5:1 for text and
3:1 for UI edges.

## Preview build

The chat-based workflow needed a single file that renders with no server, so
the game also accepts boards inlined in a
`<script type="application/json" id="starter-boards">` block. `build-preview.py`
folds `boards/` into the page to produce one. The repo copy has no such block
and reads the folder. Keep both paths working; regenerate the preview after
changing either the game or a board.

Python is the one piece of tooling this repo assumes. There is deliberately no
PowerShell port: a second copy of the same script will drift from the first,
and the drift will be found at the worst moment. If `python3` is missing, fix
that rather than working around it.

## Photos

Photos are never committed to `boards/`. `photo-sets/` is a parallel folder of
the same rosters carrying an `img` URL per card. The game does not read it. It
exists because "Paste a theme" runs the pasted list through `normalise()`,
which preserves `img`, so one paste fills a whole board.

- **Anything pasted as a URL is linked, not baked.** It shows an amber dot and
  needs the network on every load. The hub blurb promises the site works with
  no connection once loaded, which linked photos quietly break. Baking still
  requires dragging the image file onto the card one at a time.
- **Only the F1 board has a free image source.** Those are real people with
  Creative Commons photos on Wikimedia Commons, reached through
  `en.wikipedia.org/api/rest_v1/page/summary/<Page_Title>`, taking
  `thumbnail.source`. Watch for disambiguation pages: plain "George Russell"
  and "Carlos Sainz" both resolve to the wrong person.
- **The four character boards have no free source.** Disney, Ghibli, Pixar and
  Nintendo characters are all copyrighted and absent from Commons. Fan wikis
  generally refuse cross-origin canvas reads, so images dragged from one link
  rather than bake. Save the file and drag it in to get a permanent card.

## Open items

- Photos. Only the F1 board has a ready set, and even that one is linked
  rather than baked. See the Photos section above.
- Hosting is undecided. A separate repo under the same GitHub account still
  inherits the user-site custom domain, so full separation needs either its own
  `CNAME` or a different host.
- `.nojekyll` is present and empty, which keeps Pages from running Jekyll.
- The site is public once deployed. There is no auth and none is wanted.
