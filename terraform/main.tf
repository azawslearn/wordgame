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
  name     = "dockerWOrdGame"
  location = "West Europe"
}

resource "azurerm_mysql_flexible_server" "dockermysql" {
  name                   = "dockermysql"
  resource_group_name    = azurerm_resource_group.dockerWOrdGame.name
  location               = azurerm_resource_group.dockerWOrdGame.location
  administrator_login    = "mysqladminun"
  administrator_password = "EmersonFitipaldi1!"
  sku_name               = "B_Standard_B1s"
  zone                   = "3"
}

resource "azurerm_mysql_flexible_database" "dockerdb" {
  name                = "dockerdb"
  resource_group_name = azurerm_resource_group.dockerWOrdGame.name
  server_name         = azurerm_mysql_flexible_server.dockermysql.name
  charset             = "utf8"
  collation           = "utf8_unicode_ci"
}

resource "azurerm_mysql_flexible_server_firewall_rule" "allow-all-ips-rules" {
  name                = "allow-all-ips-rule"
  resource_group_name = azurerm_resource_group.dockerWOrdGame.name
  server_name         = azurerm_mysql_flexible_server.dockermysql.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
  depends_on          = [azurerm_mysql_flexible_server.functionMySQLServer]
}

output "mysql_server_fqdn" {
  description = "The Fully Qualified Domain Name of the MySQL Server."
  value       = "${azurerm_mysql_flexible_server.dockermysql.name}.mysql.database.azure.com"
}

