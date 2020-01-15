from PIL import Image

import sys
import os
import graphic_editor as ge
import kernels as ke
import numpy as np

def main():
    # Gets all needed arguments
    args = sys.argv[1:]
    
    # Checks the number of arguments and the INPUT file
    if (len(args) < 2) or (not os.path.isfile(args[-2])):
        print("[ERROR] Wrong INPUT file or missing OUTPUT file.")
        return
    
    # Checks the extension of the OUTPUT file
    if not args[-1].lower().endswith(("jpg", "jpeg", "png")):
        print("[ERROR] Bad extension of the OUTPUT file.")
        return
    
    # Loads the INPUT file
    img = np.asarray(Image.open(args[-2]), dtype=np.float)
    print("The image '" + args[-2] + "' was loaded.")
    
    # Makes a copy of the INPUT file (for unsharp masking)
    original = img.copy()
    
    # Modifies data by specified filters
    for i, arg in enumerate(args):
        if arg == "--rotate":
            img = ge.rotate(img)
            print("ROTATE finished.")
        elif arg == "--mirror":
            img = ge.mirror(img)
            print("MIRROR finished.")
        elif arg == "--inverse":
            img = ge.inverse(img)
            print("INVERSE finished.")
        elif arg == "--bw":
            img = ge.bw(img)
            print("BW finished.")
        elif arg == "--lighten":
            img = ge.lighten(img, args[i + 1])
            print("LIGHTEN finished.")
        elif arg == "--darken":
            img = ge.darken(img, args[i + 1])
            print("DARKEN finished.")
        elif arg == "--sharpen":
            img = ge.convolution(img, ke.sharpen_kernel)
            print("SHARPEN finished.")
        elif arg == "--blur":
            img = ge.convolution(img, ke.blur_kernel)
            print("BLUR finished.")
        elif arg == "--edges":
            img = ge.convolution(img, ke.edges_kernel)
            print("EDGES finished.")
        elif arg == "--emboss":
            img = ge.convolution(img, ke.emboss_kernel)
            print("EMBOSS finished.")
        elif arg == "--unsharpmask":
            img = ge.convolution(img, ke.blur_kernel)
            
            # Used SHARPEN/BLUR/EDGES/EMBOSS
            for _ in range((original.shape[0]-img.shape[0]) // 2):
                original = ge.convolution(original, ke.identity_kernel)
                
            # Used BW
            if (img.ndim == 2):
                original = ge.bw(original)
                
            img = ge.unsharpmask(img, original, args[i + 1])
            print("UNSHARPMASK finished.")

    # Saves as the OUTPUT file
    img = Image.fromarray(img.astype(np.uint8))
    img.save(args[-1])
    print("The image '" + args[-2] + "' was saved as '" + args[-1] + "'.")
    
if __name__ == "__main__":
    main()
