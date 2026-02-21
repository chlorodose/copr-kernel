outdir ?= $(PWD)
.PHONY: srpm
srpm: kernel
	dnf install -y rpkg
	cd kernel && TMPD=$$(mktemp -d) && \
	    rpkg srpm --outdir $${TMPD} --spec kernel.spec && \
		cp $${TMPD}/*.src.rpm "$(outdir)"

kernel:
	dnf install -y git find rpmdevtools
	rm -rf kernel
	git clone https://src.fedoraproject.org/rpms/kernel.git -b b60c0b3a92f7b0d3f1c19b6ad7b2baca43d723f4 --depth 1
	cd kernel && git apply ../*.patch
	find * -maxdepth 0 -type f \( -not \( -name LICENSE \) \) -and \( -not \( -name '*.patch' \) \) -exec cp {} kernel/{} \;
	cd kernel && spectool -g kernel.spec
