outdir ?= $(PWD)
.PHONY: srpm
srpm: $(notdir  $(spec)).srpm

.PHONY: kmod-nvidia-open.spec.srpm
kmod-nvidia-open.spec.srpm:
	dnf install -y curl zstd rpmdevtools
	sed "s/NV_VERSION/$$(echo $$(curl -fsSL https://github.com/chlorodose/cl-kernel/releases/download/v7.1.1/from-upstream.patch.zst | zstd -d | \
		grep -E 'NVIDIA_VERSION = [0-9]+\.[0-9]+\.[0-9]+' | cut -d '=' -f 2))/g" kmod-nvidia-open.spec >_kmod-nvidia-open.spec
	rpmbuild -bs --define "_srcrpmdir $(outdir)" _kmod-nvidia-open.spec
.PHONY: kernel.spec.srpm
kernel.spec.srpm: kernel
	dnf install -y git make gcc flex bison bzip2 rpmdevtools python3-pyyaml
	make -C kernel dist-srpm DIST= DISTRO=fedora HEAD=linux-source UPSTREAM_BRANCH=linux-source VERSION_ON_UPSTREAM=1
	cp kernel/redhat/rpm/SRPMS/*.src.rpm $(outdir)

export GIT_AUTHOR_NAME="nobody"
export GIT_AUTHOR_EMAIL="nobody@nomail"
export GIT_COMMITTER_NAME="nobody"
export GIT_COMMITTER_EMAIL="nobody@nomail"

kernel:
	dnf install -y git curl zstd
	rm -rf kernel
	git clone https://gitlab.com/cki-project/kernel-ark.git kernel -b fedora-7.1 --depth 1

	git -C kernel fetch origin refs/tags/v7.1.1 --depth 1 
	git -C kernel checkout FETCH_HEAD
	curl -fsSL https://github.com/chlorodose/cl-kernel/releases/download/v7.1.1/from-upstream.patch.zst | zstd -d | \
		git -C kernel apply -
	git -C kernel add .
	git -C kernel commit -m "" --allow-empty-message
	git -C kernel tag -a v7.1.1 -m "v7.1.1"
	git -C kernel branch linux-source v7.1.1

	git -C kernel checkout fedora-7.1
	git -C kernel cherry-pick v7.1.1
	git -C kernel apply ../0001-Add-patch-configs.patch ../adjust-default-configs.patch
	touch kernel/localversion
