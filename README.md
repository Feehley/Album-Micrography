# Micrography #
A Python3 script to pull album art and lyrics into a computer generated micrograph.
Uses the [lyricsgenius](https://pypi.org/project/lyricsgenius) API for searching albums.


### Shoutouts! ###
* Thank you!
    * [rneiss](https://github.com/rneiss/micrography)
    * [johnwmillr](https://github.com/johnwmillr/lyricsgenius)
    * FreeMono.ttf (Ubuntu Free Fonts) https://packages.ubuntu.com/bionic/all/fonts-freefont-ttf/filelist


### Setting up lyricsgenius API ###
* Go to [Genius](https://genius.com)
* Create an account
* Visit the [API Documentation Page](https://docs.genius.com/) for further API documentation
* Create an API key using the [API Clients](https://genius.com/api-clients) page
* Replace the "KEY" on line 32 and you're set!

### Setup ###
```bash
[~]> pip3 install -r requirements.txt
```

### Usage ###
#### Help Menu ####
```bash
[~]> python3 album_micrography.py -h
usage: album_micrography.py [-h] -a  -al [-f] [-fs]

Create monographs from albums!

optional arguments:
  -h, --help        show this help message and exit
  -a, --artist      Artist
  -al, --album.     Album Title
  -f, --font_style  Font Style
  -fs, --font_size  Font Size; Range: (5-50))
  -bg, --background Set Image Background Color to Black (for contrast)
  ```

#### Basic Usage  ####
```bash
[~]> python3 album_micrography.py -a Daughters -al "You Won't Get What You Want"

Searching for "You Won't Get What You Want" by Daughters...
[+] Downloading album cover!
[+] Image saved to: ./YouWontGetWhatYouWant/album_art.jpg
[+] All lyrics written to: ./YouWontGetWhatYouWant/lyrics.jpg
[+] Saving Micrograph to: YouWontGetWhatYouWant/micrograph.png
```

#### Advanced Usage ####
##### Setting Font Style #####
```bash
[~]> python3 album_micrography.py -a lizzo -al "big grrrl small world" -f ./FreeMono.ttf

Searching for "big grrrl small world" by lizzo...
[+] Downloading album cover!
[+] Image saved to: ./biggrrrlsmallworld/album_art.jpg
[+] All lyrics written to: ./biggrrrlsmallworld/lyrics.jpg
[+] Saving Micrograph to: biggrrrlsmallworld/micrograph.png
```
##### Setting Font Size #####
```bash
[~]> python3 album_micrography.py -a 'ed Sheeran' -al divide -f ./FreeMono.ttf -fs 11

Searching for "divide" by ed Sheeran...
[+] Downloading album cover!
[+] Image saved to: ./divide/album_art.jpg
[+] All lyrics written to: ./divide/lyrics.jpg
[+] Saving Micrograph to: divide/micrograph.png
```

##### Setting Background Color to Black #####
```bash
[~]> python3 album_micrography.py -a 'rage against the machine' -al 'evil empire' -bg

Searching for "evil empire" by rage against the machine
[+] Downloading album cover!
[+] Image saved to: ./evilempire/album_art.jpg
[+] All lyrics written to: ./evilempire/lyrics.jpg
[+] Saving Micrograph to: evilempire/micrograph.png
```


### Example Output ###
#### You Won't Get What You Want by Daughters ###
![You Won't Get What You Want](./examples/daughters_you_wont_get_what_you_want_micrograph.png)
#### Big Grrrl Small World by Lizzo ####
![Big Grrrl Small World](./examples/lizzo_big_grrrl_small_world_micrograph.png)
#### Divide by Ed Sheeran ####
![Divide](./examples/ed_sheeran_divide_micrograph.png)
#### Divide by Ed Sheeran ####
![Evil Empire](./examples/rage_against_the_machine_evil_empire_micrograph.png)


### Follow on steps ###
* Fix the words at the start of the image (the image starts in the middle of a sentence...)
* Create subparsers to allow for books and other mediums as well
