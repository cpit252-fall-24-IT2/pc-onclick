# Init Commit

# Interactive PC Builder System

A step-by-step system that helps users build custom PCs with real-time compatibility checking and personalized recommendations.

![Untitleddesign-ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/2a44f574-0c70-4992-82db-0ba0aa3b0a81)
### Requirements

- **Ollama**: Ensure Ollama is installed and configured. Download the required AI model:
- visit https://ollama.com/download and download the exe for ollama
- after setting it up run the following bash to download the ollama3.2 model
  ```bash
  ollama pull llama3.2
- Python: Install Python (version 3.8 or later).
- Install the required dependencies:
   - You can use `pip install -r requirements.txt`
- Run the Application: in the terminal `python main.py`

## System Overview

The PC Builder guides users through selecting and configuring PC components with automatic compatibility verification.

## Interactive Flow

### 1. Launch Screen
```
Welcome to PC ONCLICK!

Select an option to begin:
1. Start New Build
2. View Saved Build
3. Exit

User input: "1"
```

### 2. Build Type Selection
```
What type of build would you like to create?

For example, you can type:
"Gaming"
"Content Creation"
"General Purpose"
Or specify what programs you want to run or what the PC will be used for.

Please describe your needs:
User input: "I want a PC for video editing using Adobe Premiere Pro and After Effects, with some light gaming on the side."
```

### 3. Budget Setting
```
Define Your Budget:
Enter your budget (press Enter to skip):

User input: "$1500"
```

### 4. Initial Build Generation
```
Based on your use case and budget, here's your recommended build:

💻 Recommended Build:

PC Build Components

CPU: AMD Ryzen 7 5800X - $349
- Great for video editing with 8 cores/16 threads
- Strong single-core performance for gaming

GPU: NVIDIA RTX 3060 Ti - $399
- CUDA acceleration for Premiere Pro
- Capable of 1440p gaming

RAM: 32GB DDR4-3600 - $159
- Optimal for video editing workloads
- Handles multiple applications easily

Storage: 1TB NVMe SSD - $119
- Fast project loading
- Quick render times

Power Supply: 750W Gold - $109
- Efficient and reliable power delivery
- Room for future upgrades

Total: $1,135

Would you like to proceed with this build? (Yes/No)
User input: "Yes"
```




## Future Work with https://onlypc-sa.com/ar/
### 5. Component Customization
```
Would you like to modify any components?

1. CPU
2. GPU
3. RAM
4. Storage
5. Power Supply
6. Continue with current build

User input: "2"

Available GPU Alternatives:
1. NVIDIA RTX 3070 - $599
   + 20% better rendering performance
   - Exceeds current budget

2. AMD RX 6700 XT - $479
   + Similar gaming performance
   - Less efficient for Adobe suite

3. Keep current: RTX 3060 Ti - $399

Select an option (1-3):
User input: "1"
```

### 6. Compatibility Check
```
GPU updated to NVIDIA RTX 3070

⚠️ Compatibility Warning:
Current 650W PSU insufficient for RTX 3070
Recommendation: Upgrade to 750W minimum

Options:
1. Auto-adjust PSU (adds $40)
2. Choose different GPU
3. Proceed anyway (not recommended)

User input: "1"

✅ Changes applied:
- GPU updated to RTX 3070
- PSU upgraded to 750W Gold
Total cost increase: $240
```

### 7. Final Review
```
💻 Final Build Review:

Custom Content Creation Build
Total Cost: $1,375

Would you like to:
1. Save this build
2. Return to component selection
3. Start over
4. Exit

User input: "1"

Build saved successfully! You can access it later from the main menu.
Would you like to return to the main menu? (Yes/No)
User input: "Yes"
```
