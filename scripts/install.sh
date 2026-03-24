#!/bin/bash

# promptbook - Universal Installer
# "Standardizing prompts for developers, architects, and data engineers."

set -e

# --- Configuration ---
REPO_URL="https://github.com/ronmkr/Promptbook.git"
INSTALL_DIR="$HOME/.promptbook"
BIN_DIR="$HOME/.local/bin"
EXECUTABLE_NAME="promptbook"
ALIAS_NAME="pop"

# Colors for UX
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BOLD}🚀 Starting promptbook installation...${NC}\n"

# --- 1. Dependency Checks ---
echo -e "${CYAN}Checking dependencies...${NC}"

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed. Please install git and try again.${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed. Please install python3 and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Git and Python3 found.${NC}"

# --- 2. Installation ---
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Warning: $INSTALL_DIR already exists. Updating instead...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo -e "${CYAN}Cloning promptbook to $INSTALL_DIR...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# --- 3. Python Dependencies ---
echo -e "\n${CYAN}Installing Python dependencies...${NC}"
python3 -m pip install -r requirements.txt --quiet || echo -e "${YELLOW}Warning: pip install failed. You may need to install dependencies manually.${NC}"

# --- 4. Setup Executable and Alias ---
echo -e "\n${CYAN}Setting up executable...${NC}"
chmod +x "$EXECUTABLE_NAME"

# Create local bin if not exists
mkdir -p "$BIN_DIR"

# Symlink to local bin
rm -f "$BIN_DIR/$ALIAS_NAME"
rm -f "$BIN_DIR/$EXECUTABLE_NAME"
ln -s "$INSTALL_DIR/$EXECUTABLE_NAME" "$BIN_DIR/$EXECUTABLE_NAME"
ln -s "$INSTALL_DIR/$EXECUTABLE_NAME" "$BIN_DIR/$ALIAS_NAME"

# --- 5. PATH Verification ---
PATH_CHECK=$(echo "$PATH" | grep "$BIN_DIR" || true)
if [ -z "$PATH_CHECK" ]; then
    echo -e "\n${YELLOW}Note: $BIN_DIR is not in your PATH.${NC}"
    echo -e "To use '${ALIAS_NAME}' from anywhere, add this to your .zshrc or .bashrc:"
    echo -e "${BOLD}export PATH=\"\$PATH:$BIN_DIR\"${NC}"
fi

# --- 6. TUI Build (Optional) ---
if command -v cargo &> /dev/null; then
    echo -e "\n${CYAN}Rust (cargo) detected. Would you like to pre-build the TUI? (y/N)${NC}"
    read -r -p "" BUILD_TUI
    if [[ "$BUILD_TUI" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo -e "${CYAN}Building Rust TUI...${NC}"
        cd "$INSTALL_DIR/promptbook-tui"
        cargo build --release
        cd ..
    fi
fi

# --- 7. Success! ---
echo -e "\n${GREEN}${BOLD}✨ promptbook successfully installed!${NC}"
echo -e "-------------------------------------------------------"
echo -e "${BOLD}Usage:${NC}"
echo -e "  ${CYAN}${ALIAS_NAME} list${NC}          - See all prompt templates"
echo -e "  ${CYAN}${ALIAS_NAME} search <term>${NC} - Find a specific tool"
echo -e "  ${CYAN}${ALIAS_NAME}${NC}               - Launch the TUI Explorer"
echo -e "-------------------------------------------------------"
echo -e "Enjoy your standardized AI command center!\n"
