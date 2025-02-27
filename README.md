# combine-mp3

This program can be used to combine a directory of MP3 files into a single MP3
file. The directory must be named in the following format:

`2025-02-01_firstname-lastname_topic-discussed`

The program then sets the following mp3 tags:

- artist = `Firstname Lastname`
- album = `2025-02-01 - Firstname Lastname - Topic Discussed`
- title = `2025-02-01 - Firstname Lastname - Topic Discussed`
- recording date = `2025-02-01`

## Install:

- install python3
- `pip install pydub`
- `pip install mutagen`
- `pip install audioop-lts` (if Python 3.13 or newer, this may be necessary)

## To use:

`python combine-mp3.py 2025-02-01_first-last_some-topic`

## TODO:

- [ ] - support m4b
