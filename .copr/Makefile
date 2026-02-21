outdir ?= $(PWD)
.PHONY: srpm
srpm: $(notdir  $(spec)).srpm

KVER := 7.3.1
KMINOR := $(word 1,$(subst ., ,$(KVER))).$(word 2,$(subst ., ,$(KVER)))

.PHONY: kmod-nvidia-open.spec.srpm
kmod-nvidia-open.spec.srpm:
	@dnf install -y curl zstd rpmdevtools || true
	sed "s/NV_VERSION/$$(echo $$(curl -fsSL https://github.com/chlorodose/cl-kernel/releases/download/v$(KVER)/from-upstream.patch.zst | zstd -d | \
		grep -E 'NVIDIA_VERSION = [0-9]+\.[0-9]+\.[0-9]+' | cut -d '=' -f 2))/g" kmod-nvidia-open.spec >_kmod-nvidia-open.spec
	rpmbuild -bs --define "_srcrpmdir $(outdir)" _kmod-nvidia-open.spec
.PHONY: kernel.spec.srpm
kernel.spec.srpm: kernel
	@dnf install -y git make gcc flex bison bzip2 rpmdevtools python3-pyyaml openssl || true
	# Kconfig probes the openssl command when selecting ML-DSA signing keys.
	@openssl list -key-managers | grep -q ML-DSA-87 || { echo "OpenSSL with ML-DSA-87 support is required to generate kernel configs" >&2; exit 1; }
	# Use the original upstream tag as the tarball and patch baseline.
	make -C kernel dist-srpm DIST= DISTRO=fedora UPSTREAM_BRANCH=v$(KVER) VERSION_ON_UPSTREAM=0
	cp kernel/redhat/rpm/SRPMS/*.src.rpm $(outdir)

export GIT_AUTHOR_NAME="nobody"
export GIT_AUTHOR_EMAIL="nobody@nomail"
export GIT_COMMITTER_NAME="nobody"
export GIT_COMMITTER_EMAIL="nobody@nomail"

kernel:
	@dnf install -y git curl zstd || true
	rm -rf kernel
	git clone https://gitlab.com/cki-project/kernel-ark.git kernel -b fedora-$(KMINOR) --depth 1

	# Keep the upstream tag unchanged; all customizations belong to Fedora.
	git -C kernel fetch origin refs/tags/v$(KVER):refs/tags/v$(KVER) --depth 1
	curl -fsSL https://github.com/chlorodose/cl-kernel/releases/download/v$(KVER)/from-upstream.patch.zst | zstd -d | \
		git -C kernel apply -
	git -C kernel apply ../0001-Adjust-configs.patch
	touch kernel/localversion
	# genspec.sh compares the upstream tag to Git HEAD, not the working tree.
	git -C kernel add .
	git -C kernel commit -m "Apply custom kernel patches and configuration"
