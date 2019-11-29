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
    
    # Works with every pixel
    for y in range(img_h):
        for x in range(img_w):
        
            # Works with every channel
            for ch in range(channels):
                
                # Sets the height of a cut by the kernel
                y_from = y - ker_half_size
                y_to = y + ker_half_size + 1
                
                # Sets the width of the cut by the kernel
                x_from = x - ker_half_size
                x_to = x + ker_half_size + 1     
                
                # Initializes neighbours
                neighbours = np.zeros((kernel.shape[0], kernel.shape[1]), dtype = np.uint8)
                nei_y = nei_x = 0
                
                # Sets the neighbours
                for img_y in range(y_from, y_to):
                    for img_x in range(x_from, x_to):
                    
                        # Saves the neighbours or makes them as nulls if they are beyond
                        if img_y < 0 or img_x < 0 or img_y >= img_h or img_x >= img_w:
                            neighbours[nei_y][nei_x] = 0
                        else:
                            if image.ndim == 2: # GRAY
                                neighbours[nei_y][nei_x] = image[img_y][img_x]
                            else: # RGB
                                neighbours[nei_y][nei_x] = image[img_y][img_x][ch]
                        
                        nei_x += 1
                            
                    nei_y += 1
                    nei_x = 0
                           
                # Makes a sum of the neighbours
                sum = np.sum(neighbours * kernel)
                
                # Saves a new value
                if image.ndim == 2: # GRAY
                    conv_img[y][x] = int(min(max(sum, 0), 255))
                else: # RGB
                    conv_img[y][x][ch] = int(min(max(sum, 0), 255))

    return conv_img
