#!/usr/bin/env python3
"""Word-substitution codec for the PoC.
Maps (--map):
  atlas (default): 0=atlas 1=babel 2=carthage 3=delphi 4=egypt 5=fenrir 6=gaia
                   7=hades 8=ionia 9=judah a=karnak b=luxor c=myra d=nile
                   e=othrys f=paphos
  ember: 0=ember 1=frost 2=grove 3=haven 4=isle 5=jade 6=kelm 7=lark 8=moss
         9=nook a=orba b=plume c=quill d=reed e=spire f=thorn
  onyx : 0=onyx 1=pine 2=quay 3=rust 4=silk 5=talc 6=urea 7=vine 8=wave
         9=yarn a=zest b=ash c=clay d=dune e=elm f=fern
  alder: 0=alder 1=brine 2=clove 3=drift 4=elder 5=flint 6=gully 7=heath
         8=ivory 9=jasper a=kelp b=lichen c=millet d=nettle e=ochre f=prairie
Usage:
  decode: python decode_words.py [--map M] [--page] < words.txt
  encode: python decode_words.py --encode [--map M] < raw.txt
"""
import sys

MAPS = {
    "atlas": "atlas babel carthage delphi egypt fenrir gaia hades ionia judah "
             "karnak luxor myra nile othrys paphos".split(),
    "ember": "ember frost grove haven isle jade kelm lark moss nook orba plume "
             "quill reed spire thorn".split(),
    "onyx": "onyx pine quay rust silk talc urea vine wave yarn zest ash clay "
            "dune elm fern".split(),
    "alder": "alder brine clove drift elder flint gully heath ivory jasper kelp "
             "lichen millet nettle ochre prairie".split(),
}

def decode(text, page=False, name="atlas"):
    W = {w: format(i, "x") for i, w in enumerate(MAPS[name])}
    nib = "".join(W[w] for w in text.replace("-", " ").split() if w in W)
    if page:
        return "".join(chr(int(nib[i:i+4], 16)) for i in range(0, len(nib) - 3, 4))
    return bytes.fromhex(nib).decode("utf-8", "replace")

def encode(text, name="atlas"):
    return "-".join(MAPS[name][int(c, 16)] for c in text.encode("utf-8").hex())

if __name__ == "__main__":
    a = sys.argv[1:]
    name = a[a.index("--map") + 1] if "--map" in a else "atlas"
    if "--encode" in a:
        print(encode(sys.stdin.read(), name))
    else:
        print(decode(sys.stdin.read(), "--page" in a, name))
