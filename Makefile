PACKER_VERSION := 1.10.1
SHIKI_HOSTNAME := shikigotchi
SHIKI_VERSION := $(shell cut -d"'" -f2 < shikigotchi/_version.py)

MACHINE_TYPE := $(shell uname -m)
ifneq (,$(filter x86_64,$(MACHINE_TYPE)))
GOARCH := amd64
else ifneq (,$(filter i686,$(MACHINE_TYPE)))
GOARCH := 386
else ifneq (,$(filter arm64% aarch64%,$(MACHINE_TYPE)))
GOARCH := arm64
else ifneq (,$(filter arm%,$(MACHINE_TYPE)))
GOARCH := arm
else
GOARCH := amd64
$(warning Unable to detect CPU arch from machine type $(MACHINE_TYPE), assuming $(GOARCH))
endif

# The Ansible part of the build can inadvertently change the active hostname of
# the build machine while updating the permanent hostname of the build image.
# If the unshare command is available, use it to create a separate namespace
# so hostname changes won't affect the build machine.
UNSHARE := $(shell command -v unshare)
ifneq (,$(UNSHARE))
UNSHARE := $(UNSHARE) --uts
endif

# sudo apt-get install qemu-user-static qemu-utils
all: clean packer image

update_langs:
	@for lang in shikigotchi/locale/*/; do\
		echo "updating language: $$lang ..."; \
		./scripts/language.sh update $$(basename $$lang); \
	done

compile_langs:
	@for lang in shikigotchi/locale/*/; do\
		echo "compiling language: $$lang ..."; \
		./scripts/language.sh compile $$(basename $$lang); \
	done

packer: clean
	curl https://releases.hashicorp.com/packer/$(PACKER_VERSION)/packer_$(PACKER_VERSION)_linux_amd64.zip -o /tmp/packer.zip
	unzip /tmp/packer.zip -d /tmp
	sudo mv /tmp/packer /usr/bin/packer

image: clean packer
	cd builder && sudo /usr/bin/packer init combined.pkr.hcl && sudo $(UNSHARE) /usr/bin/packer build -var "shiki_hostname=$(SHIKI_HOSTNAME)" -var "shiki_version=$(SHIKI_VERSION)" combined.pkr.hcl

32bit: clean packer
	cd builder && sudo /usr/bin/packer init shikigotchi32.pkr.hcl && sudo $(UNSHARE) /usr/bin/packer build -var "shiki_hostname=$(SHIKI_HOSTNAME)" -var "shiki_version=$(SHIKI_VERSION)" shikigotchi32.pkr.hcl

64bit: clean packer
	cd builder && sudo /usr/bin/packer init shikigotchi64.pkr.hcl && sudo $(UNSHARE) /usr/bin/packer build -var "shiki_hostname=$(SHIKI_HOSTNAME)" -var "shiki_version=$(SHIKI_VERSION)" shikigotchi64.pkr.hcl

custom: clean packer
	cd builder && sudo /usr/bin/packer init shikigotchi32-custom.pkr.hcl && sudo $(UNSHARE) /usr/bin/packer build -var "shiki_hostname=$(SHIKI_HOSTNAME)" -var "shiki_version=$(SHIKI_VERSION)" shikigotchi32-custom.pkr.hcl

clean:
	- rm -rf /tmp/packer*
