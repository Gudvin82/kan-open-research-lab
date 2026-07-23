# Golos Text web font

- Upstream: <https://github.com/googlefonts/golos-text>
- Source commit: `cf2e27222937d97c2d858fff0499bcc667a64e9d`
- Source file: `fonts/variable/GolosText[wght].ttf`
- License: SIL Open Font License 1.1, preserved as `OFL.txt`
- Designers: Alexandra Korolkova and Vitaly Kuzmin
- Variable axis: `wght`, 400–900
- Coverage checked: Latin and Cyrillic

The upstream variable TTF was converted locally to one WOFF2 without subsetting:

```text
fonttools==4.60.2
fonttools ttLib.woff2 compress GolosText-Variable.ttf \
  -o GolosText-Variable.woff2
```

Result:

- size: 76,540 bytes;
- SHA-256:
  `177af0794fb0c2308b2edc76d8744549b5b390b30c67436892578c5f07c0bf00`.

The stylesheet uses `font-display: swap` and a complete system sans-serif
fallback. No runtime request is made to Google Fonts or any font CDN.
