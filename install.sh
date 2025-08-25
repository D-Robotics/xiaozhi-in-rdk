#!/bin/bash
# XiaoZhi AI Voice Assistant - RDK X5 Installation Script
# 小智AI语音助手 - RDK X5 安装脚本

set -e  # Exit on any error

echo "==============================================="
echo "🤖 XiaoZhi AI Voice Assistant - RDK X5"
echo "==============================================="
echo "📦 Starting installation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on RDK X5 or ARM64
check_platform() {
    print_status "Checking platform compatibility..."
    
    ARCH=$(uname -m)
    if [[ "$ARCH" == "aarch64" ]] || [[ "$ARCH" == "arm64" ]]; then
        print_success "ARM64 platform detected: $ARCH"
    else
        print_warning "Non-ARM platform detected: $ARCH"
        print_warning "This script is optimized for RDK X5 (ARM64)"
        read -p "Continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Installation cancelled"
            exit 1
        fi
    fi
}

# Check Python version
check_python() {
    print_status "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_success "Python $PYTHON_VERSION found"
        
        # Check if version is 3.7 or higher
        if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)'; then
            print_success "Python version is compatible"
        else
            print_error "Python 3.7+ is required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed"
        exit 1
    fi
}

# Update system packages
update_system() {
    print_status "Updating system packages..."
    
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt upgrade -y
        print_success "System packages updated"
    elif command -v yum &> /dev/null; then
        sudo yum update -y
        print_success "System packages updated (YUM)"
    else
        print_warning "Unknown package manager, skipping system update"
    fi
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    if command -v apt &> /dev/null; then
        # Ubuntu/Debian
        sudo apt install -y \
            python3-pip python3-dev python3-venv \
            build-essential \
            libasound2-dev portaudio19-dev libopus-dev libopus0 \
            alsa-utils pulseaudio-utils \
            git wget curl
        print_success "System dependencies installed (APT)"
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        sudo yum install -y \
            python3-pip python3-devel \
            gcc gcc-c++ make \
            alsa-lib-devel portaudio-devel opus-devel \
            alsa-utils pulseaudio-utils \
            git wget curl
        print_success "System dependencies installed (YUM)"
    else
        print_error "Unsupported package manager"
        exit 1
    fi
}

# Create virtual environment (optional)
create_venv() {
    print_status "Creating virtual environment..."
    
    if [[ ! -d "xiaozhi-env" ]]; then
        python3 -m venv xiaozhi-env
        print_success "Virtual environment created: xiaozhi-env"
    else
        print_warning "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source xiaozhi-env/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip
    pip3 install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        pip3 install -r requirements.txt
        print_success "Python dependencies installed from requirements.txt"
    else
        # Install manually
        pip3 install paho-mqtt==1.6.1
        pip3 install PyAudio==0.2.11
        pip3 install opuslib==3.0.1
        pip3 install cryptography==41.0.7
        pip3 install requests==2.31.0
        print_success "Python dependencies installed manually"
    fi
}

# Test audio devices
test_audio() {
    print_status "Testing audio devices..."
    
    # Check playback devices
    if aplay -l &> /dev/null; then
        print_success "Audio playback devices found:"
        aplay -l | grep -E "^card [0-9]:" | head -3
    else
        print_warning "No audio playback devices found"
    fi
    
    # Check capture devices  
    if arecord -l &> /dev/null; then
        print_success "Audio capture devices found:"
        arecord -l | grep -E "^card [0-9]:" | head -3
    else
        print_warning "No audio capture devices found"
    fi
}

# Test network connectivity
test_network() {
    print_status "Testing network connectivity..."
    
    if ping -c 1 api.tenclass.net &> /dev/null; then
        print_success "Network connectivity OK (api.tenclass.net reachable)"
    else
        print_warning "Cannot reach api.tenclass.net"
        print_warning "Please check your network connection"
    fi
}

# Set permissions
set_permissions() {
    print_status "Setting up permissions..."
    
    # Add user to audio group
    sudo usermod -a -G audio $USER
    print_success "User added to audio group"
    
    # Make script executable
    if [[ -f "xiaozhi-in-rdkx5.py" ]]; then
        chmod +x xiaozhi-in-rdkx5.py
        print_success "Script permissions set"
    fi
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    cat > run_xiaozhi.sh << 'EOF'
#!/bin/bash
# XiaoZhi AI Voice Assistant Startup Script

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [[ -d "xiaozhi-env" ]]; then
    source xiaozhi-env/bin/activate
fi

# Run XiaoZhi
python3 xiaozhi-in-rdkx5.py
EOF

    chmod +x run_xiaozhi.sh
    print_success "Startup script created: run_xiaozhi.sh"
}

# Main installation function
main() {
    echo
    print_status "Installation started at $(date)"
    echo
    
    check_platform
    check_python
    
    # Ask for virtual environment
    read -p "Create virtual environment? [Y/n] " -n 1 -r
    echo
    USE_VENV=true
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        USE_VENV=false
    fi
    
    update_system
    install_system_deps
    
    if [[ "$USE_VENV" == true ]]; then
        create_venv
    fi
    
    install_python_deps
    test_audio
    test_network
    set_permissions
    create_startup_script
    
    echo
    echo "==============================================="
    print_success "🎉 Installation completed successfully!"
    echo "==============================================="
    echo
    print_status "Next steps:"
    echo "  1. Reboot or re-login to apply group permissions"
    echo "  2. Connect USB microphone and speaker"
    echo "  3. Run: ./run_xiaozhi.sh"
    echo
    print_status "For manual start:"
    if [[ "$USE_VENV" == true ]]; then
        echo "  source xiaozhi-env/bin/activate"
    fi
    echo "  python3 xiaozhi-in-rdkx5.py"
    echo
    print_status "Troubleshooting:"
    echo "  - Check logs in xiaozhi.log"
    echo "  - Test audio: arecord -f cd -t wav -d 3 test.wav && aplay test.wav"
    echo "  - Check network: ping api.tenclass.net"
    echo
}

# Run main function
main "$@"