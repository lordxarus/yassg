Yet Another Static Site Generator

Usage:

yassg source_dir [out_dir]

 - out_dir is "public" by default

By default any markdown files placed in `source_dir/content` will be converted to HTML. everything in `source_dir/static` is copied over as if by running `cp -r source_dir/static/** out_dir/`

Set DEBUG in your environment to true to see more informative messages

TODO:
 - Configurable directories

