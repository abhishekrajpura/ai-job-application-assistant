#!/usr/bin/env python3
"""
Quick Local LLM Setup Script
Helps you get started with local LLMs quickly
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def print_header():
    print("🏠 Local LLM Quick Setup")
    print("=" * 50)
    print("This script will help you set up local LLMs for private, cost-free resume tailoring.")
    print()

def check_system_requirements():
    """Check system requirements for local LLMs"""
    print("🔍 Checking system requirements...")
    
    # Check available RAM
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)
        print(f"   RAM: {ram_gb:.1f} GB")
        
        if ram_gb < 4:
            print("   ⚠️ Warning: Less than 4GB RAM. Consider cloud LLMs instead.")
        elif ram_gb >= 8:
            print("   ✅ Good: Sufficient RAM for most local models")
        else:
            print("   ✅ OK: Can run smaller local models")
    except ImportError:
        print("   ❓ RAM check skipped (psutil not installed)")
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 9):
        print(f"   ✅ Python {python_version.major}.{python_version.minor}")
    else:
        print(f"   ❌ Python {python_version.major}.{python_version.minor} (3.9+ required)")
        return False
    
    print()
    return True

def install_ollama_option():
    """Guide user through Ollama installation"""
    print("🚀 Option 1: Ollama (Recommended)")
    print("-" * 30)
    print("Ollama is the easiest way to run local LLMs.")
    print()
    
    # Check if Ollama is already installed
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama is already installed!")
            print(f"   Version: {result.stdout.strip()}")
            
            # Check if service is running
            try:
                response = requests.get('http://localhost:11434/api/version', timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama service is running")
                    return setup_ollama_model()
                else:
                    print("⚠️ Ollama service not running")
                    print("💡 Start with: ollama serve")
            except requests.exceptions.RequestException:
                print("⚠️ Ollama service not running")
                print("💡 Start with: ollama serve")
            
            return True
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Ollama not found")
    print()
    print("📥 Installation instructions:")
    
    import platform
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("   1. Download from: https://ollama.ai/")
        print("   2. Install the .dmg file")
        print("   3. Open Terminal and run: ollama --version")
    elif system == "linux":
        print("   1. Run: curl -fsSL https://ollama.ai/install.sh | sh")
        print("   2. Verify: ollama --version")
    elif system == "windows":
        print("   1. Download from: https://ollama.ai/")
        print("   2. Install the .exe file")
        print("   3. Open Command Prompt and run: ollama --version")
    
    print()
    print("After installation, run this script again!")
    return False

def setup_ollama_model():
    """Help user pull an appropriate Ollama model"""
    print("📦 Setting up Ollama model...")
    
    # Check available models
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            available_models = result.stdout.strip()
            print("📋 Currently available models:")
            if available_models and "NAME" in available_models:
                print(available_models)
                
                # Check if llama2 is available
                if "llama2" in available_models.lower():
                    print("✅ llama2 model found - you're ready to go!")
                    return True
            else:
                print("   (No models installed)")
        
    except subprocess.TimeoutExpired:
        print("⚠️ Ollama command timed out")
        return False
    
    print()
    print("🔄 Recommended models for resume tailoring:")
    print("   • llama2 (4GB) - Good balance of speed and quality")
    print("   • llama2:13b (7GB) - Better quality, needs more RAM")
    print("   • mistral (4GB) - Fast and efficient")
    print()
    
    model_choice = input("Enter model name to install (or press Enter for 'llama2'): ").strip()
    if not model_choice:
        model_choice = "llama2"
    
    print(f"🔄 Pulling {model_choice}... (this may take several minutes)")
    try:
        result = subprocess.run(['ollama', 'pull', model_choice], 
                              timeout=600)  # 10 minutes timeout
        
        if result.returncode == 0:
            print(f"✅ Successfully installed {model_choice}!")
            return True
        else:
            print(f"❌ Failed to install {model_choice}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Model installation timed out")
        print("💡 Try again or choose a smaller model")
        return False

def setup_lmstudio_option():
    """Guide user through LM Studio setup"""
    print("🎯 Option 2: LM Studio")
    print("-" * 30)
    print("LM Studio provides a user-friendly GUI for local LLMs.")
    print()
    
    # Check if LM Studio API is running
    try:
        response = requests.get('http://localhost:1234/v1/models', timeout=2)
        if response.status_code == 200:
            models = response.json().get('data', [])
            print("✅ LM Studio API is running")
            if models:
                print(f"   {len(models)} model(s) loaded")
                return True
            else:
                print("   ⚠️ No models loaded")
                print("   💡 Load a model in LM Studio interface")
                return False
        
    except requests.exceptions.RequestException:
        pass
    
    print("❌ LM Studio not running")
    print()
    print("📥 Setup instructions:")
    print("   1. Download from: https://lmstudio.ai/")
    print("   2. Install and launch LM Studio")
    print("   3. Go to 'Discover' tab and download a model")
    print("   4. Go to 'Server' tab and start the local server")
    print("   5. Load your downloaded model")
    print()
    print("💡 Recommended models:")
    print("   • microsoft/DialoGPT-medium")
    print("   • meta-llama/Llama-2-7b-chat-hf")
    print("   • mistralai/Mistral-7B-Instruct-v0.1")
    
    return False

def setup_transformers_option():
    """Guide user through direct Transformers setup"""
    print("🔧 Option 3: Direct Transformers")
    print("-" * 30)
    print("Use Hugging Face Transformers directly (more technical).")
    print()
    
    # Check if transformers is installed
    try:
        import transformers
        import torch
        print("✅ Transformers library installed")
        print(f"   Version: {transformers.__version__}")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            print("✅ CUDA GPU available - faster inference!")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️ No CUDA GPU - will use CPU (slower)")
        
        return True
        
    except ImportError:
        print("❌ Transformers library not installed")
        print()
        print("📦 Installation:")
        print("   pip install transformers torch accelerate")
        print()
        print("💡 Models will be downloaded automatically on first use")
        return False

def update_env_file(provider: str, model: str):
    """Update .env file with local LLM settings"""
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    # Create .env from example if it doesn't exist
    if not env_path.exists() and env_example_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print("📄 Created .env file from template")
    
    if env_path.exists():
        # Read current .env
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update LLM settings
        updated_lines = []
        found_provider = False
        found_model = False
        
        for line in lines:
            if line.startswith('LOCAL_LLM_PROVIDER='):
                updated_lines.append(f'LOCAL_LLM_PROVIDER={provider}\n')
                found_provider = True
            elif line.startswith('LOCAL_LLM_MODEL='):
                updated_lines.append(f'LOCAL_LLM_MODEL={model}\n')
                found_model = True
            elif line.startswith('LLM_PROVIDER='):
                updated_lines.append('LLM_PROVIDER=local\n')
            else:
                updated_lines.append(line)
        
        # Add missing settings
        if not found_provider:
            updated_lines.append(f'LOCAL_LLM_PROVIDER={provider}\n')
        if not found_model:
            updated_lines.append(f'LOCAL_LLM_MODEL={model}\n')
        
        # Write back
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
        
        print(f"✅ Updated .env with {provider} ({model})")
    else:
        print("⚠️ No .env file found - please create one manually")

def test_setup():
    """Test the local LLM setup"""
    print("\n🧪 Testing setup...")
    print("-" * 30)
    
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        from resume.local_llm_tailor import LocalLLMResumeTailor
        
        # Test with example resume
        resume_path = "config/master_resume.json"
        if not Path(resume_path).exists():
            resume_path = "config/master_resume.json.example"
        
        if not Path(resume_path).exists():
            print("❌ No resume file found")
            print("💡 Make sure you're in the project root directory")
            return False
        
        # Get settings from .env
        provider = os.getenv('LOCAL_LLM_PROVIDER', 'ollama')
        model = os.getenv('LOCAL_LLM_MODEL', 'llama2')
        
        print(f"🔧 Testing {provider} with {model}...")
        
        tailor = LocalLLMResumeTailor(resume_path, provider, model)
        model_info = tailor.get_model_info()
        
        if model_info['model_loaded']:
            print("✅ Local LLM is working!")
            print(f"   Provider: {model_info['provider']}")
            print(f"   Model: {model_info['model_name']}")
            print(f"   Privacy: {model_info['privacy']}")
            print(f"   Cost: {model_info['cost']}")
            
            # Quick test
            sample_job = "Data Analyst position requiring Python and SQL skills."
            result = tailor.tailor_resume(sample_job, "Data Analyst")
            
            if 'error' not in result:
                print("✅ Resume tailoring test passed!")
                return True
            else:
                print(f"⚠️ Tailoring test failed: {result['error']}")
                return False
        else:
            print("❌ Local LLM not working")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print_header()
    
    if not check_system_requirements():
        print("❌ System requirements not met")
        return
    
    print("Choose your preferred local LLM option:")
    print("1. Ollama (recommended for beginners)")
    print("2. LM Studio (GUI-based)")
    print("3. Direct Transformers (advanced)")
    print("4. Skip setup")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    success = False
    provider = ""
    model = ""
    
    if choice == "1":
        success = install_ollama_option()
        provider = "ollama"
        model = "llama2"
    elif choice == "2":
        success = setup_lmstudio_option()
        provider = "lmstudio"
        model = "local-model"
    elif choice == "3":
        success = setup_transformers_option()
        provider = "transformers"
        model = "microsoft/DialoGPT-medium"
    elif choice == "4":
        print("⏭️ Setup skipped")
        return
    else:
        print("❌ Invalid choice")
        return
    
    if success:
        update_env_file(provider, model)
        
        if test_setup():
            print("\n🎉 Local LLM setup complete!")
            print("🚀 You can now use the job application bot with complete privacy!")
            print()
            print("💡 Next steps:")
            print("   python src/main.py --llm-provider local --dry-run")
            print("   python scripts/test_task2.py")
        else:
            print("\n⚠️ Setup completed but testing failed")
            print("💡 Check the documentation: docs/LOCAL_LLM_SETUP.md")
    else:
        print("\n❌ Setup incomplete")
        print("💡 See docs/LOCAL_LLM_SETUP.md for detailed instructions")

if __name__ == "__main__":
    main()