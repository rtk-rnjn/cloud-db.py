# Cloud-DB.py Changelogs

See what changed each version.

## v1.1

- Added changelogs.
- The repo is now public.
- Cleanup the code.
- Fixed a bug where the value sometimes wouldn't send.
- Better docstring for some functions.
- Setting the `return_data` kwarg to True in `.set()`
  no longer creates a extra request but instead constructs the `Result` class with the given args.
- The `number` attribute of `Result` is always available now but it's None most of the time unless the object is
  returned from the `.add()` and `.subtract()` methods.
- Added a much better real-life example in the readme.
  
### v1.0.1

Fixed a bug that prevented running anything.

### v1.0.0

First release, nothing special.