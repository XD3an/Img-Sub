# Img>Sub

A simple image steganography tool that can encode and decode messages and watermarks into and from images.

- mode：RGB

## Installation

```bash
git clone https://github.com/XD3an/Img-Sub 
pip install -r requirements.txt
```
## Usage

### TL;DR

- Encode message into image with level=0 and channel=r
```bash
python .\src\main.py --technique m>i --image .\sample\mandrill_500x480.bmp --message "Hello, World!"  --output .\result\resutl1.png
```
- Decode message from image with level=0 and channel=r where decode_size=14
```bash
python .\src\main.py --technique m<i --image .\result\resutl1.png --level 0 --channel r --decode_size 14
```
- Encode watermark into image with level=0 and channel=r
```bash
python .\src\main.py --technique w>i --image .\sample\mandrill_500x480.bmp --watermark '.\sample\nfuwm_68x68(1).jpg' --level 0 --channel r --output .\result\result2.png
```
- Decode watermark from image with level=0 and channel=r
```bash
python .\src\main.py --technique w<i --image .\result\result2.png --output .\result\result3.png
```

### Command Usage

```
    =======================================================
    =    ===================  =======      ==========  ====
    ==  =====================  =====  ====  =========  ====
    ==  ======================  ====  ====  =========  ====
    ==  ===  =  = ====   ======  ====  =======  =  ==  ====
    ==  ===        ==  =  ======  =====  =====  =  ==    ==
    ==  ===  =  =  ===    =====  ========  ===  =  ==  =  =
    ==  ===  =  =  =====  ====  ====  ====  ==  =  ==  =  =
    ==  ===  =  =  ==  =  ===  =====  ====  ==  =  ==  =  =
    =    ==  =  =  ===   ===  =======      ====    ==    ==
    =======================================================

[+] Welcome to Img>Sub!
usage: main.py [-h] [-t TECHNIQUE] [-i IMAGE] [-m MESSAGE] [-o OUTPUT] [-r] [-s SIZE] [-w WATERMARK] [-d DECODE_SIZE] [-l LEVEL] [-c CHANNEL] [-v]

Image Steganography

options:
  -h, --help            show this help message and exit
  -t TECHNIQUE, --technique TECHNIQUE
                        Technique to use (message encode into image(m>i), watermark encode into image(w>i), message decoded by image(m<i), watermark decoded by image(w<i)), etc.
  -i IMAGE, --image IMAGE
                        Image file path
  -m MESSAGE, --message MESSAGE
                        The message to be processed
  -o OUTPUT, --output OUTPUT
                        Output file path (default: ./report/output_{datetime}.png)
  -r, --random          Random message
  -s SIZE, --size SIZE  Size of message
  -w WATERMARK, --watermark WATERMARK
                        Watermark file path
  -d DECODE_SIZE, --decode_size DECODE_SIZE
                        Size of message to decode
  -l LEVEL, --level LEVEL
                        Level of Sub (bits position 7-0) (default: 0 -> LSB)
  -c CHANNEL, --channel CHANNEL
                        Channel to use (r, g, b)
  -v, --verbose         Verbose mode
```
## Analysis

### PSNR

Peak signal-to-noise ratio (PSNR) is an engineering term for the ratio between the maximum possible power of a signal and the power of corrupting noise that affects the fidelity of its representation. Because many signals have a very wide dynamic range, PSNR is usually expressed in terms of the logarithmic decibel scale.

## References

- [Hiding data in images by simple LSB substitution](https://www.sciencedirect.com/science/article/pii/S003132030300284X)
- [峰值信噪比（PSNR） - wiki](https://zh.wikipedia.org/zh-tw/%E5%B3%B0%E5%80%BC%E4%BF%A1%E5%99%AA%E6%AF%94)