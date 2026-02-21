outdir ?= $(PWD)
.PHONY: srpm
srpm: kernel
	dnf install -y rpkg
	rm -rf kernel/_target && mkdir -p kernel/_target
	cd kernel && rpkg srpm --outdir _target --spec kernel.spec
	cp kernel/_target/*.src.rpm $(outdir)

# Last 7.0
COMMIT_REF := 8ae208dec547524784a06190b766a362beaa62b4
CLONE_DEPTH := 64
kernel:
	dnf install -y git find rpmdevtools curl
	rm -rf kernel
	git clone https://src.fedoraproject.org/rpms/kernel.git --depth $(CLONE_DEPTH)
	cd kernel && git checkout $(COMMIT_REF) && git apply ../*.patch
	find * -maxdepth 0 -type f \( -not \( -name LICENSE \) \) -and \( -not \( -name '*.patch' \) \) -exec cp {} kernel/{} \;
	cd kernel && spectool -g kernel.spec
	cd kernel && curl -fsSL https://github.com/chlorodose/cl-kernel/releases/download/v7.0.0/source.tar.zst >source.tar.zst
