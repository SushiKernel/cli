#!/bin/bash

#
# by @whyakari ©2024
#

# install packages
packages() {
	sudo apt install flex bc ccache neovim -y
}

# configure clang
clang() {
	git clone https://github.com/moekernel/clang
	cd clang
	chmod +x clang.sh
	./clang.sh
	cd ../
	rm -rf clang
}

# configure gcc setup.
gcc_() {
	GCC_64_DIR="$HOME/tc/aarch64-linux-android-15.0"
	GCC_32_DIR="$HOME/tc/arm-linux-androideabi-15.0"

	if ! [ -d "${GCC_64_DIR}" ]; then
		echo "gcc not found! Cloning to ${GCC_64_DIR}..."
		if ! git clone --depth=1 -b 15 https://github.com/whyakari/aarch64-zyc-linux-gnu ${GCC_64_DIR}; then
			echo "Cloning failed! Aborting..."
			exit 1
		fi
	fi

	if ! [ -d "${GCC_32_DIR}" ]; then
		echo "gcc_32 not found! Cloning to ${GCC_32_DIR}..."
		if ! git clone --depth=1 -b 15 https://github.com/whyakari/arm-zyc-linux-gnueabi ${GCC_32_DIR}; then
			echo "Cloning failed! Aborting..."
			exit 1
		fi
	fi
}

# get kernelsu from @whyakari
kernelsu() {
    wget https://raw.githubusercontent.com/MoeKernel/scripts/ksu/ksu_update.sh
	chmod +x ksu_update.sh
	./ksu_update.sh -t stable
}

# configure kernel for compile.
kernel() {
	make mrproper
}

# get script build kernel.
moe() {
   wget https://raw.githubusercontent.com/MoeKernel/scripts/ksu/moe.sh
   chmod +x moe.sh
}

packages
clang
gcc_
kernelsu
kernel
moe
