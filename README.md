## Yet Another Static Site Generator

### Usage:

`yassg source_dir [out_dir]`

 - `out_dir` is `public/` by default

Any markdown files placed in `source_dir/content/` will be converted to HTML. everything in `source_dir/static/` is copied over as if by running `cp -r source_dir/static/. out_dir/`


Example:
 `yassg test_site && python -m http.server -d public`

Inspired by the [boot.dev](https://boot.dev) static site generator project
