import numpy as np

def add_padding(img : np.ndarray, padding_height : int, padding_width : int):
    n, m = img.shape

    padded_img = np.zeros((n + padding_height * 2, m + padding_width * 2))
    padded_img[padding_height : n + padding_height, padding_width : m + padding_width] = img

    return padded_img

def conv2d(img : np.ndarray, kernel : np.ndarray, padding=True) -> np.ndarray:
    # Dimensions
    k_height, k_width = kernel.shape
    img_height, img_width = img.shape

    # Create a padded version of the image to handle edges
    if padding == True:
        # Calculate padding required
        pad_height = k_height // 2
        pad_width = k_width // 2
        padded_img = add_padding(img, pad_height, pad_width)
    else:
        padded_img = img

    # Initialize an output image with zeros
    output = np.zeros((img_height, img_width), dtype=float)

    # Perform convolution
    for i_img in range(img_height):
        for j_img in range(img_width):
            for i_kernel in range(k_height):
                for j_kernel in range(k_width):
                    output[i_img, j_img] = output[i_img, j_img] + (padded_img[i_img+i_kernel, j_img+j_kernel] * kernel[i_kernel, j_kernel])
            output[i_img, j_img] = int(output[i_img, j_img])

    return np.array(output, dtype=np.uint8)

def conv2d_sharpening(img: np.ndarray, kernel: np.ndarray, padding=True) -> np.ndarray:
    # Dimensions
    k_height, k_width = kernel.shape
    img_height, img_width = img.shape

    # Create a padded version of the image to handle edges
    if padding:
        pad_height = k_height // 2
        pad_width = k_width // 2
        padded_img = add_padding(img, pad_height, pad_width)
    else:
        padded_img = img

    # Initialize an output image with zeros
    output = np.zeros((img_height, img_width), dtype=float)

    # Perform convolution
    for i_img in range(img_height):
        for j_img in range(img_width):
            # calcula kernel
            for i_kernel in range(k_height):
                for j_kernel in range(k_width):
                    output[i_img, j_img] += padded_img[i_img + i_kernel, j_img + j_kernel] * kernel[i_kernel, j_kernel]
    
    # Optionally clip values to valid image range
    output = np.clip(output, 0, 255)  # Garante que os valores estejam no intervalo de 0 a 255
    return np.array(output, dtype=np.float32)

def conv2d_with_lookup_table(img : np.ndarray, lookup_table : np.ndarray, padding=True, k_height=3, k_width=3) -> np.ndarray:
    if padding == True:
        padded_img = add_padding(img, k_height, k_width)

    img_height, img_width = img.shape

    # Initialize an output image with zeros
    output = np.zeros((img_height, img_width), dtype=float)

    # Perform convolution
    for i_img in range(img_height):
        for j_img in range(img_width):
            for i_kernel in range(k_height):
                for j_kernel in range(k_width):
                    p = padded_img[i_img+i_kernel, j_img+j_kernel]
                    output[i_img, j_img] = output[i_img, j_img] + (p * lookup_table[int(p)])
            output[i_img, j_img] = int(output[i_img, j_img])

    output = np.clip(output, 0, 255)
    return np.array(output, dtype=np.uint8)

if __name__ == '__main__':
    # Imagem exemplo (5x5)
    img = np.array([[1, 2, 3, 4, 5],
                    [6, 7, 8, 9, 10],
                    [11, 12, 13, 14, 15],
                    [16, 17, 18, 19, 20],
                    [21, 22, 23, 24, 25]], dtype=np.uint8)

    # Adiciona padding de 1 pixel em torno da imagem
    padded_img = add_padding(img, 1, 1)

    print(padded_img)

