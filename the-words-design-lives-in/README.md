# The words design lives in.

A generative data visualization of the 41 course descriptions in SCAD Graphic Design (GRDS) and Graphic Design and Visual Experience (GDVX), 2026–2027 catalog. It was made as a practice piece for the Generative Communication course.

Each ring is one course description, ordered from 201 at the center to 792 at the edge. Thirty-seven design keywords carry their own hue, lighter as they recur, and a line joins every pair of matching words, 2,353 in all. Strategy courses, grounded in discourse, turn 36 degrees clockwise at each step. Literacy courses, grounded in visual praxis, turn 72 degrees counterclockwise. Every line is redrawn at each step, and their movement together is Synthesis. Ten steps, ten posters, one generative system.

## Folders

- The live web version is `index.html` at the top of this repository, published at intentcollective.design/data. Its menu offers two motion modes, Tick and Flow, each of the ten posters, the MP4, and downloads. A line weight slider lets viewers explore the system from 0.25 to 2 pt. The designer’s authored value is 1 pt, and the posters and downloads always stay at 1 pt. The page holds still on poster 01 when the viewer has reduced motion turned on.
- `motion` holds the motion poster, 1440 × 2040 px, H.264, 30 fps, 10 seconds, seamless loop.
- `downloads` holds the files offered on the website. `pdf` has print-ready A1 PDFs with fonts embedded. `svg` has SVGs with fonts built in, for use on websites. `png` has 1440 × 2040 images for portfolio platforms and social media. `zip` has all ten posters in each format.
- `web-layers` holds the two ring layers the website rotates, one for Strategy courses and one for Literacy courses.
- `posters/A1` holds the ten final static posters as editable source files, A1 portrait (594 × 841 mm), one per frame.
- `posters/A0` holds the A0 layout template the series was developed from.
- `frames-png` holds each frame as a 1440 × 2040 PNG and a contact sheet of all ten.
- `process` holds earlier studies, from the first fixed-size rings to the line weight tests.
- `data` holds the course data (`courses.json`), the keyword ranking with counts and colors (`keyword_ranking.csv`), and every keyword’s position on its ring (`keyword_positions.json`).
- `source` holds the Python scripts that generate the rings, lines, and frames.

## Typefaces

Barlow (Regular, Medium, SemiBold, Bold) from Google Fonts. Install it before opening the SVG files in Illustrator. The Intent Collective wordmark uses Adobe Garamond Pro Bold, and falls back to EB Garamond on the web.

## Notes on the source

The scripts were written for a working session and still contain absolute file paths. They document the logic of the system more than they offer a ready-made tool.

© Henry Kim, Intent Collective
