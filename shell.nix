{ pkgs ? import <nixpkgs> {} }:

let
	pythonEnv = pkgs.python312.withPackages (ps: with ps; [
		pillow
		numpy
		numba
		raylib-python-cffi
		black
		isort
		pynvim
		jax
		jaxtyping
		mypy
		ruff
		ipython
		pydantic
	]);
in

	pkgs.mkShell {
		name = "my-python-devshell";

		buildInputs = with pkgs; [
			pythonEnv
			nodejs
			pyright        # Use the top-level pyright derivation
			neovim
			git
		];

		shellHook = ''
	    echo "Environment ready: Python, Pyright, Ruff, Neovim"
	    '';
	}
