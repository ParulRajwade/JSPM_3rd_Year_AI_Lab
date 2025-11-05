import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, models
from PIL import Image
import copy
import os
import argparse

def run_style_transfer(content_path, style_path, output_path, num_steps, style_weight, content_weight, imsize_arg):
    """
    Main function to execute the neural style transfer.
    """
    os.environ['TORCH_HOME'] = './'

    # Check for a GPU, and set the device to use.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # --- 1. Configuration & Image Loading ---

    # Define the image size. Larger images require more memory and processing time.
    if imsize_arg is None:
        imsize = 512 if torch.cuda.is_available() else 256
        print(f"Image size not specified, using default based on device: {imsize}")
    else:
        imsize = imsize_arg
        print(f"Using specified image size: {imsize}")

    # Image transformations: resize and convert to a tensor.
    loader = transforms.Compose([
        transforms.Resize((imsize, imsize)),
        transforms.ToTensor(),
    ])

    # Function to load an image and apply transformations.
    def load_image(image_name):
        try:
            image = Image.open(image_name)
        except (IOError, FileNotFoundError):
            print(f"Error: Could not open the image file at '{image_name}'. Please check the path.")
            exit()
        # Add a fake batch dimension required for the network's input.
        image = loader(image).unsqueeze(0)
        return image.to(device, torch.float)

    # Load content and style images
    print(f"Loading content image: {content_path}")
    content_img = load_image(content_path)
    
    print(f"Loading style image: {style_path}")
    style_img = load_image(style_path)

    # The target image is initialized as a clone of the content image.
    # This helps the optimization converge faster.
    target_img = content_img.clone()

    # --- 2. Model and Feature Extraction ---

    # Load a pre-trained VGG-19 model. We only need the feature extraction part.
    vgg = models.vgg19(weights=models.VGG19_Weights.DEFAULT).features.to(device).eval()

    # The VGG network is trained on images normalized with specific mean and std.
    # We must use the same normalization for our images.
    class Normalization(nn.Module):
        def __init__(self, mean, std):
            super(Normalization, self).__init__()
            # Reshape mean and std to [C, 1, 1] to make them broadcastable
            self.mean = torch.tensor(mean).view(-1, 1, 1).to(device)
            self.std = torch.tensor(std).view(-1, 1, 1).to(device)

        def forward(self, img):
            # normalize img
            return (img - self.mean) / self.std

    # Define the layers to use for content and style loss.
    # These are the names of the layers in VGG-19.
    content_layers_default = ['conv_4']
    style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']

    def get_style_model_and_losses(cnn, style_img, content_img):
        cnn = copy.deepcopy(cnn)
        
        # Normalization module
        normalization = Normalization(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
        
        content_losses = []
        style_losses = []

        model = nn.Sequential(normalization)

        i = 0  # increment every time we see a conv
        for layer in cnn.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = f'conv_{i}'
            elif isinstance(layer, nn.ReLU):
                name = f'relu_{i}'
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = f'pool_{i}'
            elif isinstance(layer, nn.BatchNorm2d):
                name = f'bn_{i}'
            else:
                raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

            model.add_module(name, layer)

            if name in content_layers_default:
                # Add content loss:
                target = model(content_img).detach()
                content_loss = ContentLoss(target)
                model.add_module(f"content_loss_{i}", content_loss)
                content_losses.append(content_loss)

            if name in style_layers_default:
                # Add style loss:
                target_feature = model(style_img).detach()
                style_loss = StyleLoss(target_feature)
                model.add_module(f"style_loss_{i}", style_loss)
                style_losses.append(style_loss)

        # Now we trim off the layers after the last content and style losses
        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
                break
                
        model = model[:(i + 1)]
        
        return model, style_losses, content_losses

    # --- 3. Loss Functions ---

    class ContentLoss(nn.Module):
        def __init__(self, target,):
            super(ContentLoss, self).__init__()
            self.target = target.detach()
            self.criterion = nn.MSELoss()

        def forward(self, input):
            self.loss = self.criterion(input, self.target)
            return input

    def gram_matrix(input):
        batch_size, num_channels, height, width = input.size()
        features = input.view(batch_size * num_channels, height * width)
        G = torch.mm(features, features.t())
        # Normalize by the number of elements in the feature map
        return G.div(batch_size * num_channels * height * width)

    class StyleLoss(nn.Module):
        def __init__(self, target_feature):
            super(StyleLoss, self).__init__()
            self.target = gram_matrix(target_feature).detach()
            self.criterion = nn.MSELoss()

        def forward(self, input):
            G = gram_matrix(input)
            self.loss = self.criterion(G, self.target)
            return input

    # --- 4. The Optimization Loop ---

    # Tell the optimizer which tensor to optimize. In our case, it's the target image.
    # Note: The model's parameters are frozen.
    target_img.requires_grad_(True)
    optimizer = optim.LBFGS([target_img]) # LBFGS is often recommended for NST.

    unloader = transforms.ToPILImage()

    def save_image(tensor, filename):
        image = tensor.cpu().clone()
        image = image.squeeze(0) # Remove the batch dimension
        image = unloader(image)
        image.save(filename)

    print("Building the style transfer model...")
    model, style_losses, content_losses = get_style_model_and_losses(vgg, style_img, content_img)
    model.requires_grad_(False) # Freeze the model parameters

    print(f"Optimizing for {num_steps} steps...")
    run = [0]
    while run[0] <= num_steps:

        def closure():
            # Correct the values of updated input image
            target_img.data.clamp_(0, 1)

            optimizer.zero_grad()
            model(target_img)
            
            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run[0] += 1
            if run[0] % 50 == 0:
                print(f"run {run[0]}:")
                print(f'Style Loss : {style_score.item():4f} Content Loss: {content_score.item():4f}')
                # Save intermediate images
                base, ext = os.path.splitext(output_path)
                intermediate_filename = f"{base}_step{run[0]}{ext}"
                save_image(target_img, intermediate_filename)

            return style_score + content_score

        optimizer.step(closure)

    # --- 5. Final Result ---

    # A final clamp to ensure pixel values are valid
    target_img.data.clamp_(0, 1)

    print(f"\nOptimization finished. Saving final image to {output_path}")
    save_image(target_img, output_path)

if __name__ == '__main__':
    # --- CLI Argument Parsing ---
    parser = argparse.ArgumentParser(description='Neural Style Transfer using PyTorch.')
    
    parser.add_argument('content_image', type=str, help='Path to the content image.')
    parser.add_argument('style_image', type=str, help='Path to the style image.')
    
    parser.add_argument('--output_image', type=str, default='final_output.png', 
                        help='Path to save the output image (default: final_output.png).')
                        
    parser.add_argument('--imsize', type=int, default=None, 
                        help='Size to resize images to. Defaults to 512 for GPU, 256 for CPU.')
                        
    parser.add_argument('--steps', type=int, default=300, 
                        help='Number of optimization steps (default: 300).')
                        
    parser.add_argument('--style_weight', type=float, default=1000000, 
                        help='Weight for the style loss (default: 1000000).')
                        
    parser.add_argument('--content_weight', type=float, default=1, 
                        help='Weight for the content loss (default: 1).')

    args = parser.parse_args()

    # Run the main style transfer function with parsed arguments
    run_style_transfer(
        content_path=args.content_image,
        style_path=args.style_image,
        output_path=args.output_image,
        num_steps=args.steps,
        style_weight=args.style_weight,
        content_weight=args.content_weight,
        imsize_arg=args.imsize
    )