resource "azurerm_resource_group" "main" {
  name     = "${var.project}-rg"
  location = var.location
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.project}-vn"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "main" {
  name                 = "${var.project}-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_public_ip" "main" {
  name                = "${var.project}-public-ip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Static"

  domain_name_label = "${var.project}-app"
}

resource "azurerm_network_interface" "main" {
  name                = "${var.project}-network-interface"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }
}

resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.project}-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B2ats_v2"
  admin_username      = var.vm-username

  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  disable_password_authentication = false
  admin_password                  = var.vm-password

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_id = "/subscriptions/${var.azure_subscription_id}/resourceGroups/${var.image-rg}/providers/Microsoft.Compute/images/${var.image}"

  custom_data = base64encode(templatefile("${path.module}/first-run.sh.tpl", {
    frontend-url      = "http://${azurerm_public_ip.main.domain_name_label}.${azurerm_public_ip.main.location}.cloudapp.azure.com"
    database-url      = azurerm_key_vault_secret.database-url.value
    jwt-secret        = azurerm_key_vault_secret.jwt-secret.value
    osu-client-secret = azurerm_key_vault_secret.osu-client-secret.value
  }))

  identity {
    type = "SystemAssigned"
  }
}


resource "azurerm_network_security_group" "main" {
  name                = "${var.project}-security_group"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "allowssh"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allowhttp"
    priority                   = 200
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    environment = "Production"
  }
}


resource "azurerm_subnet_network_security_group_association" "main" {
  subnet_id                 = azurerm_subnet.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_key_vault" "main" {
  name                       = "${var.project}kv"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  rbac_authorization_enabled = false
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  purge_protection_enabled   = false

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id # Your specific account ID

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
      "Purge",
      "Recover"
    ]
  }
}

# resource "azurerm_key_vault_access_policy" "terraform_admin" {
#   key_vault_id = azurerm_key_vault.main.id
#   tenant_id    = data.azurerm_client_config.current.tenant_id
#   object_id    = data.azurerm_client_config.current.object_id
#
#   key_permissions = [
#     "Create",
#     "Get",
#   ]
#
#   secret_permissions = [
#     "Set",
#     "Get",
#     "Delete",
#     "Purge",
#     "Recover"
#   ]
# }

# resource "azurerm_key_vault_access_policy" "vm_reader" {
#   key_vault_id = azurerm_key_vault.main.id
#   tenant_id    = data.azurerm_client_config.current.tenant_id
#   object_id    = azurerm_linux_virtual_machine.main.id
#
#
#   secret_permissions = [
#     "Get",
#     "List",
#   ]
# }


resource "azurerm_key_vault_secret" "database-url" {
  name         = "database-url"
  value        = var.database-url
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "osu-client-secret" {
  name         = "osu-client-secret"
  value        = var.osu-client-secret
  key_vault_id = azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "jwt-secret" {
  name         = "jwt-secret"
  value        = var.jwt-secret
  key_vault_id = azurerm_key_vault.main.id
}

// TODO: find a way to get the .env variables + VM public IP to the variables
