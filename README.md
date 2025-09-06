## Yet Another Static Site Generator

### Installation:
`pip install yassg-lx`

### Usage:
`yassg source_dir [out_dir]`

Example:
`yassg test_site && python -m http.server -d public`
 
Any Markdown files placed in `source_dir/content/` will be converted to HTML. Everything in `source_dir/static/` is copied to `out_dir/`

`out_dir` is `./public/` by default

### Development
```
git clone https://github.com/lordxarus/yassg
pip install --editable .
```

Inspired by the [boot.dev](https://boot.dev) static site generator project
