# Local LLM Setup Guide

Complete guide to setting up and using local Large Language Models for resume tailoring. Get full privacy, no API costs, and complete control over your data.

## 🏠 Why Local LLMs?

- **🔒 Complete Privacy**: All data stays on your machine
- **💰 Zero API Costs**: No ongoing subscription fees
- **⚡ Fast Response**: No network latency once loaded
- **🎯 Customizable**: Fine-tune models for your specific needs
- **📶 Offline Capable**: Works without internet connection

## 🚀 Option 1: Ollama (Recommended)

**Ollama** is the easiest way to run local LLMs. It handles model management and provides a simple API.

### Installation

#### Windows/Mac
1. Download from [ollama.ai](https://ollama.ai/)
2. Install the application
3. Open terminal and verify: `ollama --version`

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Setup

1. **Start Ollama**:
   ```bash
   ollama serve
   ```

2. **Pull a recommended model**:
   ```bash
   # For good performance (4GB+ RAM recommended)
   ollama pull llama2

   # For better quality (8GB+ RAM recommended)
   ollama pull llama2:13b

   # For best quality (16GB+ RAM recommended)
   ollama pull llama2:70b

   # Alternative: Code-focused model
   ollama pull codellama
   ```

3. **Test the model**:
   ```bash
   ollama run llama2
   # Type a message and press Enter to test
   # Type /bye to exit
   ```

### Integration with Job Bot

Update your `.env` file:
```bash
# Local LLM Configuration
LOCAL_LLM_PROVIDER=ollama
LOCAL_LLM_MODEL=llama2
```

Test with the job bot:
```bash
python src/resume/local_llm_tailor.py
```

## 🎯 Option 2: LM Studio

**LM Studio** provides a user-friendly GUI for running local models.

### Installation

1. Download from [lmstudio.ai](https://lmstudio.ai/)
2. Install and launch the application

### Setup

1. **Download a model** in LM Studio:
   - Go to "Discover" tab
   - Search for models like:
     - `microsoft/DialoGPT-medium` (smaller, faster)
     - `huggingface/CodeBERTa-small-v1` (code-focused)
     - `meta-llama/Llama-2-7b-chat-hf` (general purpose)

2. **Start the local server**:
   - Go to "Server" tab
   - Click "Start Server"
   - Note the port (usually 1234)

3. **Load a model**:
   - Select your downloaded model
   - Click "Load Model"

### Integration with Job Bot

Update your `.env` file:
```bash
# Local LLM Configuration
LOCAL_LLM_PROVIDER=lmstudio
LOCAL_LLM_MODEL=your-loaded-model-name
LM_STUDIO_URL=http://localhost:1234
```

## 🔧 Option 3: Direct Transformers

Run models directly using the Transformers library. More technical but gives maximum control.

### Setup

1. **Install dependencies**:
   ```bash
   pip install transformers torch accelerate
   ```

2. **Choose a model** (examples):
   - `microsoft/DialoGPT-medium` - Good for conversation
   - `facebook/opt-1.3b` - General purpose, medium size
   - `EleutherAI/gpt-neo-1.3B` - Alternative to GPT

### Integration with Job Bot

Update your `.env` file:
```bash
# Local LLM Configuration
LOCAL_LLM_PROVIDER=transformers
LOCAL_LLM_MODEL=microsoft/DialoGPT-medium
```

## ⚙️ Configuration Options

Add these to your `.env` file:

```bash
# === LOCAL LLM SETTINGS ===

# Provider: ollama, lmstudio, or transformers
LOCAL_LLM_PROVIDER=ollama

# Model name (depends on provider)
LOCAL_LLM_MODEL=llama2

# Optional: Custom API endpoints
OLLAMA_URL=http://localhost:11434
LM_STUDIO_URL=http://localhost:1234

# Performance settings
LOCAL_LLM_TEMPERATURE=0.3
LOCAL_LLM_MAX_TOKENS=2000
LOCAL_LLM_TIMEOUT=120

# Fallback behavior
LOCAL_LLM_FALLBACK=smart  # smart, mock, or cloud
```

## 🎯 Recommended Models by Use Case

### **💼 For Resume Tailoring (Recommended)**
- **Ollama**: `llama2` or `mistral`
- **LM Studio**: `microsoft/DialoGPT-medium`
- **Transformers**: `facebook/opt-1.3b`

### **💻 For Technical Jobs**
- **Ollama**: `codellama`
- **LM Studio**: `microsoft/codebert-base`
- **Transformers**: `microsoft/CodeBERTa-small-v1`

### **📊 For Data Analysis Jobs**
- **Ollama**: `llama2:13b` (if you have 8GB+ RAM)
- **LM Studio**: Any Llama-2 variant
- **Transformers**: `EleutherAI/gpt-neo-1.3B`

## 🔍 Testing Your Setup

1. **Test basic functionality**:
   ```bash
   cd ai-job-application-assistant
   python src/resume/local_llm_tailor.py
   ```

2. **Test with the main application**:
   ```bash
   python scripts/test_task2.py
   ```

3. **Test resume tailoring**:
   ```bash
   python src/main.py --dry-run --llm-provider local
   ```

## 🚀 Performance Tips

### **Memory Requirements**
- **Small models** (1-3B parameters): 4GB+ RAM
- **Medium models** (7-13B parameters): 8GB+ RAM  
- **Large models** (30B+ parameters): 16GB+ RAM

### **Speed Optimization**
- **GPU Acceleration**: Use CUDA-compatible GPU for faster inference
- **Model Quantization**: Use 4-bit or 8-bit quantized models
- **Batch Processing**: Process multiple resumes at once

### **Quality vs Speed**
- **Fastest**: Small models like DialoGPT-medium
- **Balanced**: Llama2 7B or Mistral 7B
- **Best Quality**: Llama2 13B+ (requires more RAM)

## 🛠️ Troubleshooting

### **Common Issues**

1. **"Model not found" error**:
   ```bash
   # For Ollama
   ollama pull llama2
   
   # Check available models
   ollama list
   ```

2. **"Connection refused" error**:
   ```bash
   # Make sure Ollama is running
   ollama serve
   
   # Or restart LM Studio server
   ```

3. **Out of memory errors**:
   - Use a smaller model (e.g., DialoGPT-medium instead of Llama2)
   - Close other applications
   - Use quantized models

4. **Slow response times**:
   - Use GPU acceleration if available
   - Try smaller models
   - Reduce max_tokens in configuration

### **Performance Issues**

1. **Model loading is slow**:
   - First load always takes time (downloading/caching)
   - Keep Ollama/LM Studio running in background
   - Use SSD storage for better I/O

2. **Inference is slow**:
   - Check if GPU is being used: `nvidia-smi` (NVIDIA GPUs)
   - Try quantized models (4-bit/8-bit versions)
   - Reduce context length

### **Quality Issues**

1. **Poor resume tailoring quality**:
   - Try a larger model (Llama2 13B vs 7B)
   - Adjust temperature setting (lower = more focused)
   - Use domain-specific models for technical jobs

2. **Invalid JSON responses**:
   - The system has smart fallbacks for this
   - Try different temperature settings
   - Consider fine-tuning for your specific format

## 📊 Model Comparison

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| DialoGPT-medium | 1GB | 4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Quick testing |
| Llama2 7B | 4GB | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | General use |
| Llama2 13B | 7GB | 16GB | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Best quality |
| CodeLlama | 4GB | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Tech jobs |
| Mistral 7B | 4GB | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Balanced |

## 🔄 Switching Between Models

You can easily switch between different local LLM setups:

### **Quick Switch via Environment Variables**
```bash
# Use Ollama with Llama2
export LOCAL_LLM_PROVIDER=ollama
export LOCAL_LLM_MODEL=llama2

# Use LM Studio
export LOCAL_LLM_PROVIDER=lmstudio
export LOCAL_LLM_MODEL=your-model

# Use direct Transformers
export LOCAL_LLM_PROVIDER=transformers
export LOCAL_LLM_MODEL=microsoft/DialoGPT-medium
```

### **Test Different Models**
```bash
# Test all available providers
python src/resume/local_llm_tailor.py

# Test specific provider
python -c "
from src.resume.local_llm_tailor import LocalLLMResumeTailor
tailor = LocalLLMResumeTailor('config/master_resume.json', 'ollama', 'llama2')
print(tailor.get_model_info())
"
```

## 📈 Advanced Features

### **Custom Model Fine-tuning**
For advanced users, you can fine-tune models specifically for resume tailoring:

1. **Collect training data**: Job descriptions + tailored resumes
2. **Use tools like**: LoRA, QLoRA for efficient fine-tuning
3. **Train on**: Domain-specific resume/job matching

### **Hybrid Approach**
Combine local and cloud LLMs:

```bash
# Use local for privacy-sensitive tasks
LOCAL_LLM_PROVIDER=ollama

# Fallback to cloud for complex tasks
OPENAI_API_KEY=your_key_here
LOCAL_LLM_FALLBACK=cloud
```

### **Batch Processing**
Process multiple resumes efficiently:

```python
from src.resume.local_llm_tailor import LocalLLMResumeTailor

tailor = LocalLLMResumeTailor('config/master_resume.json')
jobs = [
    {"title": "Data Analyst", "description": "..."},
    {"title": "Business Analyst", "description": "..."}
]

results = tailor.batch_tailor_resumes(jobs)
```

## 🎯 Next Steps

1. **Choose your preferred option** (Ollama recommended for beginners)
2. **Install and test** the local LLM setup
3. **Update your `.env` file** with local LLM configuration
4. **Run the test script** to verify everything works
5. **Start using** your private, cost-free AI resume tailor!

## 🆘 Need Help?

- **Ollama Documentation**: [ollama.ai/docs](https://ollama.ai/docs)
- **LM Studio Guide**: [lmstudio.ai/docs](https://lmstudio.ai/docs)
- **Transformers Documentation**: [huggingface.co/transformers](https://huggingface.co/transformers)
- **GitHub Issues**: [Report problems here](https://github.com/abhishekrajpura/ai-job-application-assistant/issues)

Happy local LLM tailoring! 🚀