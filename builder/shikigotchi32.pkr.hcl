packer {
  required_plugins {
    arm = {
      version = "1.0.0"
      source  = "github.com/cdecoux/builder-arm"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = ">= 1.1.1"
    }
  }
}

variable "shiki_hostname" {
  type = string
}

variable "shiki_version" {
  type = string
}

source "arm" "rpi32-shikigotchi" {
  file_checksum_url             = "https://downloads.raspberrypi.com/raspios_oldstable_lite_armhf/images/raspios_oldstable_lite_armhf-2024-03-12/2024-03-12-raspios-bullseye-armhf-lite.img.xz.sha256"
  file_urls                     = ["https://downloads.raspberrypi.com/raspios_oldstable_lite_armhf/images/raspios_oldstable_lite_armhf-2024-03-12/2024-03-12-raspios-bullseye-armhf-lite.img.xz"]
  file_checksum_type            = "sha256"
  file_target_extension         = "xz"
  file_unarchive_cmd            = ["unxz", "$ARCHIVE_PATH"]
  image_path                    = "../shikigotchi-32bit.img"
  qemu_binary_source_path       = "/usr/libexec/qemu-binfmt/arm-binfmt-P"
  qemu_binary_destination_path  = "/usr/libexec/qemu-binfmt/arm-binfmt-P"
  image_build_method            = "resize"
  image_size                    = "9G"
  image_type                    = "dos"
  image_partitions {
    name         = "boot"
    type         = "c"
    start_sector = "8192"
    filesystem   = "fat"
    size         = "256M"
    mountpoint   = "/boot"
  }
  image_partitions {
    name         = "root"
    type         = "83"
    start_sector = "532480"
    filesystem   = "ext4"
    size         = "0"
    mountpoint   = "/"
  }
}
build {
  name = "Shikigotchi 32 Bit"
  sources = ["source.arm.rpi32-shikigotchi"]
  provisioner "file" {
    destination = "/usr/bin/"
    sources     = [
      "data/32bit/usr/bin/bettercap-launcher",
      "data/32bit/usr/bin/hdmioff",
      "data/32bit/usr/bin/hdmion",
      "data/32bit/usr/bin/monstart",
      "data/32bit/usr/bin/monstop",
      "data/32bit/usr/bin/shikigotchi-launcher",
      "data/32bit/usr/bin/shikilib",
    ]
  }
  provisioner "shell" {
    inline = ["chmod +x /usr/bin/*"]
  }

  provisioner "file" {
    destination = "/etc/systemd/system/"
    sources     = [
      "data/32bit/etc/systemd/system/bettercap.service",
      "data/32bit/etc/systemd/system/shikigotchi.service",
      "data/32bit/etc/systemd/system/shikigrid-peer.service",
    ]
  }
  provisioner "file" {
    destination = "/etc/update-motd.d/01-motd"
    source      = "data/32bit/etc/update-motd.d/01-motd"
  }
  provisioner "shell" {
    inline = ["chmod +x /etc/update-motd.d/*"]
  }
  provisioner "shell" {
    inline = ["apt-get -y --allow-releaseinfo-change update", "apt-get -y dist-upgrade", "apt-get install -y --no-install-recommends ansible"]
  }
  provisioner "ansible-local" {
    command         = "ANSIBLE_FORCE_COLOR=1 PYTHONUNBUFFERED=1 SHIKI_VERSION=${var.shiki_version} SHIKI_HOSTNAME=${var.shiki_hostname} ansible-playbook"
    extra_arguments = ["--extra-vars \"ansible_python_interpreter=/usr/bin/python3\""]
    playbook_dir    = "extras/"
    playbook_file   = "shikigotchi32.yml"
  }
}