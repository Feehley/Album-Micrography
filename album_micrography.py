#!/usr/bin/env python3

from string import punctuation, digits
from requests import get
from json import loads
from shutil import copyfileobj
from argparse import ArgumentParser
from os import path, mkdir
from PIL import Image, ImageColor, ImageDraw, ImageFont
from lyricsgenius import Genius # https://github.com/johnwmillr/LyricsGenius


def download_image(output_dir, url):
    extension = url.split('.')[-1]
    filename = f"./{output_dir}/album_art.{extension}"
    r = get(url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as fptr:
            copyfileobj(r.raw, fptr)
    else:
        print(f"[!] Status Code: {r.status_code}")
        return None
    return filename


def get_album(output_dir, artist_name, album_name):
    filename = f"./{output_dir}/lyrics.txt"
    try:
        genius = Genius(
            'KEY',
            skip_non_songs=True,
            excluded_terms=["(Remix)", "(Live)"],
            remove_section_headers=True)
        album = loads(genius.search_album(album_name, artist_name).to_json())

        print("[+] Downloading album cover!")
        album_art_url = album['cover_art_url']
        album_art = download_image(output_dir, album_art_url)
        if album_art != None:
            print(f"[+] Album art saved to: {album_art}")

        lyrics_arr = []
        for tracks in album['tracks']:
            lyrics = tracks['song']['lyrics'].split('\n')[1:]
            lyrics[-1] = lyrics[-1].replace('Embed', '').rstrip(digits)
            lyrics = ' '.join(lyrics)
            lyrics_arr.append(lyrics)

        with open(f"{filename}", 'w') as fptr:
            fptr.write(' '.join(lyrics_arr))
    except Exception as inst:
        filename  = None
        album_art = None
        print(f"[!] Error: {inst}")
    return filename, album_art


def get_args():
    parser = ArgumentParser(description="Create monographs from albums!")
    parser.add_argument('-a',
                        '--artist',
                        help     = "Artist",
                        metavar  = '\b',
                        required = True)
    parser.add_argument('-al',
                        '--album',
                        help     = "Album Title",
                        metavar  = '\b',
                        required = True)
    parser.add_argument('-f',
                        '--font_style',
                        help     = "Font Style",
                        metavar  = '\b',
                        default  = "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
                        required = False)
    parser.add_argument('-fs',
                        '--font_size',
                        help     = "Font Size; Range: (5-50))",
                        metavar  = '\b',
                        type     = int,
                        default  = 10,
                        choices  = range(5, 50),
                        required = False)
    parser.add_argument('-bg',
                        '--background',
                        help     = "Set Image Background Color to Black (for contrast)",
                        action   = "store_true", 
                        default  = False, 
                        required = False)
    

    args = parser.parse_args()
    return args


def main():
    #set some more variables. These probably shouldn't be mucked with too much.
    fontDrawSize = 18
    imgMargin = 10
    sampleDensity=1

    args = get_args()
    artist_name = args.artist
    album_name  = args.album
    fontSize    = args.font_size
    font        = ImageFont.truetype(args.font_style, fontDrawSize)
    bg          = args.background

    output_dir      = f"{''.join(album_name.split('.')[-1]).replace(' ', '_')}"
    output_dir      = output_dir.translate(str.maketrans('', '', punctuation)).replace(' ', '_')
    destinationFile = f"{output_dir}/micrograph.png"

    # Make directory for temporary storage
    if not path.isdir(output_dir):
        mkdir(output_dir)


    filename, album_art = get_album(output_dir, artist_name, album_name)
    if filename != None and album_name != None:
        print(f"[+] All lyrics written to: {filename}")
    else:
        print("[!] Something went wrong!  Try a different album")
        exit(-1)

    # text input
    with open(filename, 'r') as fptr:
        text = fptr.read()
        text = text[::-1]

    # image input
    sample = Image.open(album_art)
    width, height = sample.size

    #set pixel density to = 8.5"/11" @ ~300 dpi (i.e. width [330] * fontsize [10] / pixel density of 1), and resize other side to fit,
    if (width > height):
        basewidth = 330
        wpercent = (basewidth/float(sample.size[0]))
        hsize = int((float(sample.size[1])*float(wpercent)))
        sample = sample.resize((basewidth,hsize), Image.ANTIALIAS)
        width, height = sample.size

    else:
        baseheight = 300
        hpercent = (baseheight/float(sample.size[1]))
        wsize = int((float(sample.size[0])*float(hpercent)))
        sample = sample.resize((wsize,baseheight), Image.ANTIALIAS)

        width, height = sample.size

    #output init
    outputImageSize = (width*fontSize//sampleDensity+imgMargin,height*fontSize//sampleDensity+imgMargin)
    imgBgColor = max(sample.getcolors(sample.size[0]*sample.size[1]))[1]
    if bg: 
        imgBgColor = (0, 0, 0)
    outputImage = Image.new("RGB", outputImageSize, color=imgBgColor)
    draw = ImageDraw.Draw(outputImage)

    #cycle through each pixel, get the color, place the next letter in the text
    index = 0
    for y in range(0,height,sampleDensity):
        for x in range (width-1,0,-sampleDensity):  #this goes from width to 0 rather than vice versa to properly place hebrew
            color = sample.getpixel((x,y))

            if color != imgBgColor:
                try:
                    draw.text((x*fontSize//sampleDensity,
                               y*fontSize//sampleDensity),
                               text[index%len(text)], font=font, fill=color)

                    index += 1
                except (IndexError):
                    index = 0

    #save image
    print(f"[+] Saving Micrograph to: {destinationFile}")
    outputImage.save(destinationFile)

    return


if __name__ == '__main__':
    main()
