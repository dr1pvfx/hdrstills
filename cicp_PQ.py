import sys
from PIL import Image, PngImagePlugin

# adds a cICP chunk to PNG files to specify color gamut and HDR brightness.
# This example uses the sample BT2020 + PQ cICP chunk from https://w3c.github.io/PNG-spec/#11cICP
# Requires Pillow >8.0.0. See https://github.com/python-pillow/Pillow/pull/4292
# View the resulting PNG in an app that supports cICP chunks, such as Chrome 105+
# (https://chromium-review.googlesource.com/c/chromium/src/+/3705739)
# For more information about CICP, see https://github.com/AOMediaCodec/libavif/wiki/CICP

def putchunk_hook(fp, cid, *data):
    if cid == b"haxx":
        cid = b"cICP"
    return PngImagePlugin.putchunk(fp, cid, *data)


with Image.open(sys.argv[1]) as im:
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add(b"haxx", bytes([9, 16, 0, 1]))
    im.encoderinfo = {"pnginfo": pnginfo}
    with open(sys.argv[2], "wb") as outfile:
        PngImagePlugin._save(im, outfile, sys.argv[2], chunk=putchunk_hook)