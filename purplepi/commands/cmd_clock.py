from purplepi.cli import pass_environment

import click
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime


@click.command("clock", short_help="Shows PyFiglet Clock in MiniTFT display.")
@pass_environment
def cli(ctx):
    """Shows Clock in MiniTFT display."""
    ctx.log("PurplePi Clock")
    ctx.vlog("DEBUG")

    #     time_string = datetime.datetime.now().strftime(time_format)

    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 64000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the ST7789 display:
    disp = st7789.ST7789(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
        width=135,
        height=240,
        x_offset=53,
        y_offset=40,
    )

    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
    image = Image.new("RGB", (width, height))
    rotation = 270


    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0


    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 52)

    # Turn on the backlight
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    # Time Format
    time_format = '%H:%M:%S'

    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Shell scripts for system monitoring from here:
        time_string = datetime.datetime.now().strftime(time_format)

        # Write four lines of text.
        y = top
        draw.text((x, y), time_string, font=font, fill="#FFFFFF")
        # y += font.getsize(IP)[1]
        # draw.text((x, y), CPU, font=font, fill="#FFFF00")
        # y += font.getsize(CPU)[1]
        # draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        # y += font.getsize(MemUsage)[1]
        # draw.text((x, y), Disk, font=font, fill="#0000FF")
        # y += font.getsize(Disk)[1]
        # draw.text((x, y), Temp, font=font, fill="#FF00FF")

        # Display image.
        disp.image(image, rotation)
        time.sleep(0.1)