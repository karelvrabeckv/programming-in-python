import numpy as np

def apply_filter(image: np.array, kernel: np.array) -> np.array:

    # A given image has to have either 2 (grayscale) or 3 (RGB) dimensions
    assert image.ndim in [2, 3]
    
    # A given filter has to be 2 dimensional and square
    assert kernel.ndim == 2
    assert kernel.shape[0] == kernel.shape[1]

    # Gets a width and height of the given image
    img_h = image.shape[0];
    img_w = image.shape[1];

    # Gets a distance from a middle to an edge of the given kernel
    ker_half_size = int(kernel.shape[0] / 2)
    
    # Gets a number of channels and initializes a final image
    conv_img = channels = None;
    if image.ndim == 2: # GRAY
        channels = 1
        conv_img = np.zeros((img_h, img_w), dtype = np.uint8)
    else: # RGB
        channels = image.shape[2]
        conv_img = np.zeros((img_h, img_w, channels), dtype = np.uint8)

    # Declares neighbours
    neighbours = np.zeros((kernel.shape[0], kernel.shape[1]), dtype = np.uint8)
    
    # Works with every pixel
    for y in range(img_h):
        for x in range(img_w):
        
            # Works with every channel
            for ch in range(channels):
                
                # Sets the height of a cut by the kernel
                y_from = y - ker_half_size
                y_to = y + ker_half_size
                
                # Sets the width of the cut by the kernel
                x_from = x - ker_half_size
                x_to = x + ker_half_size
                
                # Detects borders and sets paddings
                top_padd = bottom_padd = left_padd = right_padd = 0
                
                if (y_from < 0):
                    top_padd = -y_from
                    y_from = 0
                
                if (y_to > img_h - 1):
                    bottom_padd = y_to - (img_h - 1)
                    y_to = img_h
                    
                if (x_from < 0):
                    left_padd = -x_from
                    x_from = 0
                
                if (x_to > img_w - 1):
                    right_padd = x_to - (img_w - 1)
                    x_to = img_w

                # Gets neighbours
                if image.ndim == 2: # GRAY
                    neighbours = image[y_from:y_to + 1, x_from:x_to + 1]
                else: # RGB
                    neighbours = image[y_from:y_to + 1, x_from:x_to + 1, ch]
                
                # Fills zeros if needed
                neighbours = np.pad(
                    neighbours,
                    ((top_padd, bottom_padd), (left_padd, right_padd)),
                    'constant'
                )
                
                # Makes a sum of the neighbours
                sum_of_neighbours = np.sum(neighbours * kernel)
                
                # Saves a new value
                if image.ndim == 2: # GRAY
                    conv_img[y][x] = int(min(max(sum_of_neighbours, 0), 255))
                else: # RGB
                    conv_img[y][x][ch] = int(min(max(sum_of_neighbours, 0), 255))

    return conv_img
