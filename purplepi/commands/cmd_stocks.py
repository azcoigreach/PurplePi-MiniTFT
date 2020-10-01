from purplepi.cli import pass_environment

import click
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import datetime
import yfinance as yf


@click.command("stocks", short_help="Shows Stocks in MiniTFT display.")
@pass_environment
def cli(ctx):
    """Shows Clock in MiniTFT display."""
    ctx.log("Purple Stocks")
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
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

    # Turn on the backlight
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    
    while True:
        # Draw a black filled box to clear the image.
        

        # get stock quotes from yfinance
        tickers = ["^DJI", "^GSPC", "^IXIC", "MSFT", "AAPL", "TSLA", "NFLX", "DIS", "QQQ", "SPY", "NVDA", "WORK", "WMT", "QCOM", "ZM", "F", "PBR", "SIRI"]
        ctx.log("Displaying Tickers: " + str(tickers))
        for ticker in tickers:
            # Clear screen
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            # Reset top line
            y = top
            quote_color = "#C7C7C7"

            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            close_quote = (data.tail(1)['Close'].iloc[0]) # Current close quote
            open_quote = (data.tail(2)['Close'].iloc[0]) # Close quote from previous day
            diff_quote = close_quote - open_quote # Close quote minus open quote
            diff_quote = '{0:+.2f}'.format(diff_quote) # format diff_quote to 2 decimal places
            
            if close_quote < open_quote:
                quote_color = "#FF0000"  # RED
            elif close_quote > open_quote:
                quote_color = "#00FF00"  # GREEN
            
            ctx.log(ticker + " O:" + str(open_quote) + " C:" + str(close_quote) + " D:" + str(diff_quote))
            ctx.vlog(data)
            
            draw.text((x, y), str(ticker), font=font, fill="#0000FF")
            y += font.getsize(ticker)[1]
            draw.text((x, y), str(close_quote), font=font, fill=quote_color)
            y += font.getsize(str(close_quote))[1]
            draw.text((x, y), str(diff_quote), font=font_small, fill="#C7C7C7")

            disp.image(image, rotation)
            time.sleep(5)

        # y += font.getsize(CPU)[1]
        # draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        # y += font.getsize(MemUsage)[1]
        # draw.text((x, y), Disk, font=font, fill="#0000FF")
        # y += font.getsize(Disk)[1]
        # draw.text((x, y), Temp, font=font, fill="#FF00FF")

        # Display image.
        ctx.log("Reload Stocks")
        # time.sleep(1)