import numpy as np

# 'ROTATE' filter
def rotate(img: np.array):
    new_img = np.rot90(img, -1)
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# 'MIRROR' filter
def mirror(img: np.array):
    new_img = np.flip(img, 1) # 0 -> horizontally, 1 -> vertically
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# 'INVERSE' filter
def inverse(img: np.array):
    new_img = 255 - img
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# 'BW' filter
def bw(img: np.array):
    new_img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# 'LIGHTEN' filter
def lighten(img: np.array, percentage):
    # Checks the data type of the percentage
    if not percentage.lstrip("-").isdigit():
        print("[ERROR] Bad LIGHTEN syntax.")
        return img
        
    # Checks the scope of the percentage
    if (int(percentage) < 0) or (int(percentage) > 100):
        print("[ERROR] Only values from 0 to 100 for LIGHTEN.")
        return img

    new_img = img * (1+int(percentage) / 100)
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)

    return new_img
 
# 'DARKEN' filter
def darken(img: np.array, percentage):
    # Checks the data type of the percentage
    if not percentage.lstrip("-").isdigit():
        print("[ERROR] Bad DARKEN syntax.")
        return img
        
    # Checks the scope of the percentage
    if (int(percentage) < 0) or (int(percentage) > 100):
        print("[ERROR] Only values from 0 to 100 for DARKEN.")
        return img

    new_img = img * (int(percentage) / 100)
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# 'UNSHARPMASK' filter
def unsharpmask(img: np.array, original: np.array, amount):
    # Checks the data type of the amount
    if not amount.lstrip("-").isdigit():
        print("[ERROR] Bad UNSHARPMASK syntax.")
        return img
        
    # Checks the scope of the amount
    if (int(amount) < 0) or (int(amount) > 100):
        print("[ERROR] Only values from 0 to 100 for UNSHARPMASK.")
        return img
        
    # Due to the combination with other filters
    img = img.astype(np.float)
    
    new_img = (original + (original-img)*float(amount))
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# Includes 'SHARPEN', 'BLUR', 'EDGES' and 'EMBOSS' filters
def convolution(img: np.array, kernel: np.array):
    # Due to the combination with other filters
    img = img.astype(np.float)
    
    if (len(img.shape) == 2): # GRAY
        x, y = img.shape
        new_img = np.zeros([x - 2, y - 2])
        new_img = modify(img, kernel)
    else: # RGB
        x, y, z = img.shape
        new_img = np.zeros([x - 2, y - 2, z])
        new_img[..., 0] = modify(img[..., 0], kernel)
        new_img[..., 1] = modify(img[..., 1], kernel)
        new_img[..., 2] = modify(img[..., 2], kernel)
        
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)
    
    return new_img

# Modifies all pixels by counting and storing the sum of their neighbours
def modify(img: np.array, kernel: np.array):
    new_img = np.zeros(img.shape[:2])
    new_img = (
        kernel[0]*img[0:-2, 0:-2]
        + kernel[1]*img[0:-2, 1:-1]
        + kernel[2]*img[0:-2, 2:  ]
        + kernel[3]*img[1:-1, 0:-2]
        + kernel[4]*img[1:-1, 1:-1]
        + kernel[5]*img[1:-1, 2:  ]
        + kernel[6]*img[2:  , 0:-2]
        + kernel[7]*img[2:  , 1:-1]
        + kernel[8]*img[2:  , 2:  ]
    )

    return new_img
    