# 🎨 AI Image Generator


---

## 🌟 Project Overview

Yeh ek simple, interactive aur full-stack web application hai jo **Stable Diffusion v1.5** machine learning model ka use karke user ke text prompt se digital art generate karta hai.

Is project mein **Frontend (HTML/CSS/JS)** aur **Backend (Python Flask)** ko jodkar ek complete solution demonstrate kiya gaya hai.

### Key Features
* **Text-to-Image Generation:** User prompts se images generate karta hai.
* **Customization:** Users pre-defined **Styles** (e.g., Photography, Anime, Digital Art) aur **Aspect Ratio** (1:1, 16:9) select kar sakte hain.
* **Download Option:** Generated image ko turant download karne ki facility.
* **VRAM Optimization:** **NVIDIA 2060 (4GB VRAM)** jaise limited resources ke liye optimize kiya gaya hai, jismein `float16` precision aur OOM (Out of Memory) error handling shamil hai.

---

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript | User interface aur backend se communication. |
| **Backend** | Python, Flask | API endpoints aur server management. |
| **AI Model** | Stable Diffusion v1.5 | Core image generation logic. |
| **Libraries** | PyTorch (CUDA), Diffusers, Flask-CORS | GPU access, model handling, aur cross-origin communication. |

---

## 🚀 Local Setup Instructions

Project ko apne local machine par run karne ke liye yeh steps follow karein:

### Prerequisites (Zaroori Chizein)
1.  **Python 3.8+**
2.  **NVIDIA GPU** with proper **CUDA** installation (essential for fast generation).
3. **Python libraries** pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121) 
pip install diffusers transformers accelerate flask flask-cors Pillow

### 1. Repository Clone Karein
Terminal mein apne project ko download karein:
```bash
git clone [https://github.com/Kishankr77/Text-to-Image.git]
AI-Generator