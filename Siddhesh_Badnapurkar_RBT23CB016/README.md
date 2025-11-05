# PyTorch Neural Style Transfer

A command-line tool to apply the artistic style of one image to the content of another, using a pre-trained VGG-19 network with PyTorch. This project is an implementation of the paper "A Neural Algorithm of Artistic Style" by Gatys et al.


## Features

-   **Command-Line Interface**: Easily specify content, style, and output images from your terminal.
-   **Customizable Parameters**: Adjust the number of optimization steps, image size, and the weights of content and style loss.
-   **GPU Acceleration**: Automatically uses a CUDA-enabled GPU if available for significantly faster processing.
-   **Pre-trained VGG-19**: Leverages the powerful feature extraction capabilities of the VGG-19 model, no training required.
-   **Intermediate Results**: Saves progress images every 50 steps, allowing you to monitor the optimization process.

## Requirements

-   Python 3.11+
-   PyTorch
-   TorchVision
-   Pillow (PIL Fork)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/51ddhesh/Neural-Style-Transfer
    cd Neural-Style-Transfer
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    uv venv
    source .venv/bin/activate 
    ```

3.  **Install the required packages:**
    ```bash
    uv pip install torch torchvision Pillow
    # or
    uv pip install -r requirements.txt
    ```
    *Note: For GPU support, please follow the official PyTorch installation instructions for your specific CUDA version.*

4.  **Download your images:**
    Place the content and style images you want to use in the project directory or provide the full path to them.

## Usage

The script is run from the command line, with the content and style images as required arguments.

### Basic Usage

To run the style transfer with default settings, simply provide the paths to your content and style images.

```bash
python3 main.py path/to/content_image.jpg path/to/style_image.jpg
```

This will create an output file named `final_output.png` in the current directory.

### Advanced Usage

You can customize the process using optional flags.

```bash
python3 main.py content.jpg style.jpg --output_image my_artwork.png --steps 500 --imsize 512 --style_weight 500000
```

This command will:
-   Use `content.jpg` and `style.jpg` as input.
-   Save the final image as `my_artwork.png`.
-   Run the optimization for 500 steps.
-   Resize the images to 512x512 pixels.
-   Set the style loss weight to 500,000.

## Command-Line Arguments

Here is a full list of available arguments:

| Argument | Shorthand | Description | Default |
| :--- | :--- | :--- | :--- |
| `content_image` | | (Positional) Path to the content image. | **Required** |
| `style_image` | | (Positional) Path to the style image. | **Required** |
| `--output_image` | | Path to save the output image. | `final_output.png` |
| `--imsize` | | Size to resize images to. Defaults to 512 for GPU, 256 for CPU. | `None` |
| `--steps` | | Number of optimization steps. | `300` |
| `--style_weight` | | Weight for the style loss. | `1000000` |
| `--content_weight`| | Weight for the content loss. | `1` |

To see all options from the command line, run:
```bash
python3 main.py -h
```

## How It Works

The algorithm uses a pre-trained convolutional neural network (VGG-19) to separate the *content* and *style* representations of an image.

-   **Content Representation**: The feature maps from the deeper layers of the network are used to capture the high-level content of an image. The *content loss* is the mean-squared error between the feature maps of the content image and the generated image.

-   **Style Representation**: The style is captured by the correlations between different filter responses in the network's layers. These correlations are calculated using a Gram matrix. The *style loss* is the mean-squared error between the Gram matrices of the style image and the generated image.

The process starts with an image (a copy of the content image) and iteratively updates its pixels to minimize both the content loss and the style loss, effectively blending the content of one image with the style of another.

## Acknowledgments

-   This implementation is based on the paper [A Neural Algorithm of Artistic Style](https://arxiv.org/abs/1508.06576) by Leon A. Gatys, Alexander S. Ecker, and Matthias Bethge.
-   The code structure is heavily inspired by the official PyTorch tutorial on [Neural Transfer Using PyTorch](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html).