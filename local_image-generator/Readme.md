# AI Image Generator - README

## Overview

This project demonstrates how to generate AI images locally using Stable Diffusion models. You can create high-quality images from text prompts completely for free on your own computer. The repository includes scripts for running both the older Stable Diffusion 2.1 model (lighter, faster) and the newer Stable Diffusion 3.5 model (higher quality, more resource-intensive).

## What You Can Create

- **Any image from text prompts**: Generate unlimited images from any text description
- **High quality outputs**: Using Stable Diffusion 3.5 for photorealistic results
- **Fast generation**: With a compatible GPU, images can be generated in seconds to minutes
- **Complete control**: Adjust prompts, image dimensions, inference steps, and more

## Prerequisites

Before you begin, ensure you have the following:

### Required Software
- **Python 3.8+** installed on your system
- **Code Editor** (VS Code recommended)
- **Git** (optional, for cloning the repository)

### Hardware Requirements
- **Option 1 - NVIDIA GPU (Recommended)**:
  - NVIDIA GPU with CUDA support
  - 8GB+ VRAM for 2.1 model
  - 16GB+ VRAM for 3.5 model
  - NVIDIA CUDA Toolkit installed

- **Option 2 - CPU Only**:
  - Works but will be significantly slower
  - 16GB+ RAM recommended
  - Generation time: 20-30 minutes per image

### Account Requirements
- **Hugging Face Account**: Required to access the Stable Diffusion 3.5 model (free)

## Setup Instructions

### Step 1: Create a Hugging Face Account

1. Go to [Hugging Face](https://huggingface.co/)
2. Click "Sign Up" and create your free account
3. Navigate to the Stable Diffusion 3.5 model page
4. Accept the license agreement to gain access

### Step 2: Install NVIDIA CUDA (For GPU Users)

If you have an NVIDIA GPU:
1. Visit the [NVIDIA CUDA Toolkit download page](https://developer.nvidia.com/cuda-downloads)
2. Download and install the latest version for your operating system
3. Verify installation by running `nvcc --version` in your terminal

### Step 3: Clone the Repository

```bash
git clone [repository-url]
cd [repository-name]
```

Alternatively, download the repository as a ZIP file and extract it.

### Step 4: Set Up Virtual Environment

Create and activate a virtual environment to isolate dependencies:

**Windows:**
```bash
python -m venv env
.\env\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### Step 5: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 6: Install PyTorch

Visit the [PyTorch website](https://pytorch.org/) and select:
- Your operating system (Windows, Mac, Linux)
- Package manager: pip
- Language: Python
- Compute platform: CUDA (if you have an NVIDIA GPU) or CPU

Copy and run the provided installation command. For example:
```bash
# For CUDA (NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# For CPU only
pip install torch torchvision torchaudio
```

**Important**: Install PyTorch after installing the other dependencies to ensure the correct version is installed.

### Step 7: Set Up Hugging Face Authentication

1. Go to your Hugging Face [Settings](https://huggingface.co/settings) → Access Tokens
2. Click "Create New Token"
3. Name your token (e.g., "local_generation")
4. Select "Read" access
5. Copy the token
6. In your terminal, authenticate:

```bash
huggingface-cli login
# Paste your token when prompted
# Answer "Y" to add as git credential
```

## Running the Scripts

### Option 1: Stable Diffusion 2.1 (Faster, Less Resource-Intensive)

This model works well on most systems and generates images quickly:

```bash
python 2-1.py
```

**Customization Options:**
- Modify the `prompts` list to add your own text descriptions
- Adjust `num_inference_steps` (higher = better quality but slower)
- Change `pipe.to("cuda")` to `pipe.to("cpu")` if you don't have a GPU

### Option 2: Stable Diffusion 3.5 (Higher Quality, More Resource-Intensive)

This model produces significantly better images but requires a powerful GPU:

```bash
python 3-5.py
```

**Customization Options:**
- Edit the `prompt` variable with your desired text
- Adjust `num_inference_steps` for quality/speed tradeoff
- Change `pipe.to("cuda")` to `pipe.to("cpu")` if using CPU (warning: very slow)

**Performance Notes:**
- On an RTX 4090, generating one image takes ~1.5 minutes
- CPU generation can take 20-30 minutes per image
- The model is approximately 16GB to download

## How It Works

### The Technology

1. **Stable Diffusion**: A deep learning model that generates images from text descriptions
2. **Diffusion Process**: The model starts with random noise and iteratively refines it to match your text prompt
3. **Inference Steps**: Each step gradually improves image quality; more steps = better results

### Code Structure

- **`2-1.py`**: Script for Stable Diffusion 2.1 model
- **`3-5.py`**: Script for Stable Diffusion 3.5 model
- **`requirements.txt`**: List of Python dependencies
- **`README.md`**: This documentation

### Key Parameters

| Parameter | Description | Impact |
|-----------|-------------|--------|
| `prompt` | Text description of desired image | Determines output content |
| `num_inference_steps` | Number of refinement steps | Higher = better quality, slower |
| `height` / `width` | Image dimensions in pixels | Larger = more detail, slower |
| `device` | "cuda" or "cpu" | GPU = faster, CPU = slower |

## Troubleshooting

### Common Issues

**"CUDA not available" error:**
- Ensure CUDA Toolkit is properly installed
- Verify PyTorch was installed with CUDA support
- Run `python -c "import torch; print(torch.cuda.is_available())"` to test

**Hugging Face authentication errors:**
- Make sure you've logged in with `huggingface-cli login`
- Check that you've accepted the model license agreement
- Verify your token has read permissions

**Out of memory errors:**
- Try reducing image dimensions
- Reduce batch size (if generating multiple images)
- Close other applications using GPU memory

**Slow generation:**
- Use the 2.1 model for faster results
- Reduce `num_inference_steps`
- Ensure you're using GPU (CUDA) and not CPU

## Best Practices

1. **Start with 2.1 model**: Test prompts and settings with the faster model first
2. **Optimize prompts**: Be specific and descriptive for better results
3. **Step tuning**: Start with 20 steps, increase gradually for quality
4. **Resource management**: Close other GPU-intensive applications
5. **Regular updates**: Keep dependencies and models updated

## Customization Examples

### Multiple Prompts (2.1 Model)
```python
prompts = [
    "a capybara holding a sign saying hello world",
    "a cyberpunk character with tattoos in a rainy alley",
    "a mystical wetland with forests"
]
```

### Single Prompt (3.5 Model)
```python
prompt = "a Roman soldier standing outside a Coliseum at sunset"
```

## Performance Expectations

| Setup | 2.1 Model Time | 3.5 Model Time |
|-------|---------------|---------------|
| RTX 4090 | ~3 seconds | ~90 seconds |
| RTX 3080 | ~5 seconds | ~3 minutes |
| CPU (high-end) | ~2 minutes | ~20-30 minutes |
| CPU (average) | ~5 minutes | ~45-60 minutes |

## Support

- Check the GitHub repository's README for updates
- Consult the Hugging Face documentation for Stable Diffusion
- Verify all software versions are compatible

## License

This project uses models from Hugging Face. Please respect the license agreements of the respective models.

---

**Happy image generating!** 🎨✨
