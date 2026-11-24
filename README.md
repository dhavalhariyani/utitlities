# Utilities

Small tools and reference pages, published with GitHub Pages.

## Layout

```
index.html              landing page listing every tool
tools/<tool-name>/      one folder per tool
  index.html            the page itself
  data/                 data files the page links to
  scripts/              scripts that generate the page/data
.nojekyll               serve files as-is (no Jekyll build)
```

## Tools

| Tool | Description |
|------|-------------|
| [sonal-audio-events](tools/sonal-audio-events/) | Groups videos from the Sonal Audio Old Bhajan YouTube channel into single-night programs, with per-singer sections. |
| [kandas-bapu-channels](tools/kandas-bapu-channels/) | Searchable full listings and single-night programs for the Raju Mokaria and Naran Valani YouTube channels. |

To add a tool, create `tools/<name>/index.html` and add a link to the root `index.html` and to the table above.
