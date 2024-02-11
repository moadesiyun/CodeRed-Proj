# CodeRed-Proj

## How to Contribute

### With Nix

1. Install Nix:
- Linux: Check your distro's package manager or follow the instructions [here](https://nixos.org/download.html#nix-install-linux).
- MacOS: Follow the instructions [here](https://nixos.org/download.html#nix-install-macos).
- Windows: First, set up [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) if you haven't already. Then, check your distro's package manager or follow the instructions [here](https://nixos.org/download.html#nix-install-windows) within your WSL environment.

2. Clone this repo:
```shell
git clone https://github.com/moadesiyun/CodeRed-Proj.git
```
3. Enter the development shell:
```shell
cd CodeRed-Proj
nix develop
```

### Without Nix

1. Install dependencies:
```shell
pip install -r requirements.txt
```

### Testing

- Everything:
```shell
python main.py
```

- Gemini:
```shell
python basic.py
```
