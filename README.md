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

4. Create an environment variable named `GOOGLE_API_KEY` containing your [Google API key](https://makersuite.google.com/app/apikey).
```shell
export GOOGLE_API_KEY=<your api key> # you will probably need to do this every time you reopen your terminal
```

### Without Nix
1. Clone this repo:
```shell
git clone https://github.com/moadesiyun/CodeRed-Proj.git
```

2. Create and activate virtual environment:
```
cd CodeRed-Proj
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```shell
pip install -r requirements.txt
```

4. Create an environment variable named `GOOGLE_API_KEY` containing your [Google API key](https://makersuite.google.com/app/apikey).
```shell
export GOOGLE_API_KEY=<your api key> # you will probably need to do this every time you reopen your terminal
```

### Testing

- Everything:
```shell
python main.py
```

- Gemini:
```shell
python web/generator.py
```
