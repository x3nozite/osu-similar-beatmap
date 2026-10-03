packer{
  required_plugins{
    azure = {
      source = "github.com/hashicorp/azure"
      version = "~> 2"
    }
  }
}

source "azure-arm" "ubuntu" {
  use_azure_cli_auth = true
  subscription_id = "562645fb-48aa-4696-a4e3-8564a3500183"

  azure_tags = {
    project = "osu-similarity"
  }

  image_offer                       = "0001-com-ubuntu-server-jammy"
  image_publisher                   = "canonical"
  image_sku                         = "22_04-lts"
  location                          = "Central India"

  managed_image_name                = "osu_similarity-ubuntu-docker-base"
  managed_image_resource_group_name = "osu_similarity-rg"

  os_type                           = "Linux"
  tenant_id                         = "3485b963-82ba-4a6f-810f-b5cc226ff898"
  vm_size                           = "Standard_B2ats_v2"
}

build {
  name = "osu_similarity-img"
  sources = ["source.azure-arm.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg",
      "sudo install -m 0755 -d /etc/apt/keyrings",
      "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
      "sudo chmod a+r /etc/apt/keyrings/docker.asc",
      "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
      "sudo apt update",
      "sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin",
      "sudo usermod -aG docker $(whoami)",
      "sudo waagent -force -deprovision+user && export HISTSIZE=0 && sync"
    ]
  }
}
