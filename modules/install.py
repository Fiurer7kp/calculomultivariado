# install.py - Script de instalación automática
import os
import sys
import subprocess

def check_pip():
    """Verifica si pip está disponible"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_requirements():
    """Instala los requerimientos"""
    requirements = [
        "streamlit==1.28.0",
        "sympy==1.12", 
        "plotly==5.15.0",
        "numpy==1.24.0",
        "pandas==2.0.0"
    ]
    
    print("🚀 Instalando dependencias...")
    
    for package in requirements:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"✅ {package} instalado correctamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {package}: {e}")

if __name__ == "__main__":
    if not check_pip():
        print("❌ pip no está disponible. Instalando pip...")
        try:
            import ensurepip
            ensurepip.bootstrap()
            print("✅ pip instalado correctamente")
        except Exception as e:
            print(f"❌ Error instalando pip: {e}")
            sys.exit(1)
    
    install_requirements()
    print("\n🎉 ¡Todas las dependencias instaladas!")
    print("\n📝 Para ejecutar la aplicación:")
    print("streamlit run app.py")