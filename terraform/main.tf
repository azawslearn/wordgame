terraform {
  backend "azurerm" {
    storage_account_name = "storageforterraform1"
    container_name       = "tfstate1"
    key                  = "17"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "dockerWOrdGame" {
  name     = "functionRG"
  location = "West Europe"
}

resource "azurerm_mysql_flexible_server" "docker_mysql" {
  name                   = "docker_mysql"
  resource_group_name    = azurerm_resource_group.functionRG.name
  location               = azurerm_resource_group.functionRG.location
  administrator_login    = "mysqladminun"
  administrator_password = "EmersonFitipaldi1!"
  sku_name               = "B_Standard_B1s"
  zone                   = "3"
}

resource "azurerm_mysql_flexible_database" "docker_db" {
  name                = "users"
  resource_group_name = azurerm_resource_group.functionRG.name
  server_name         = azurerm_mysql_flexible_server.functionMySQLServer.name
  charset             = "utf8"
  collation           = "utf8_unicode_ci"
}

resource "azurerm_mysql_flexible_server_firewall_rule" "allow_all_ips" {
  name                = "allow-all-ips-rule"
  resource_group_name = azurerm_resource_group.functionRG.name
  server_name         = azurerm_mysql_flexible_server.functionMySQLServer.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
  depends_on          = [azurerm_mysql_flexible_server.functionMySQLServer]
}

output "mysql_server_fqdn" {
  description = "The Fully Qualified Domain Name of the MySQL Server."
  value       = "${azurerm_mysql_flexible_server.docker_mysql.name}.mysql.database.azure.com"
}

