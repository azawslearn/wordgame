// Define parameters
param prefix string = 'mysq3'
param location string = 'eastus'
param adminUser string = 'azureuser'
param vmPassword string = 'P@ssw0rd!'

// Define variables
var vmName = '${prefix}UbuntuVM'
var vnetName = '${prefix}VNet'
var subnetName = '${prefix}Subnet'
var nsgName = '${prefix}NSG'
var publicIpName = '${prefix}PublicIP'
var nicName = '${prefix}NIC'

// Define variables for second VM
var secondVmName = '${prefix}UbuntuVM2'
var secondNicName = '${prefix}NIC2'
var secondPublicIpName = '${prefix}PublicIP2'

// Create Network Security Group
resource nsg 'Microsoft.Network/networkSecurityGroups@2020-11-01' = {
  name: nsgName
  location: location
  properties: {
    securityRules: [
      {
        name: 'AllowAll'
        properties: {
          priority: 100
          access: 'Allow'
          direction: 'Inbound'
          protocol: '*'
          sourcePortRange: '*'
          sourceAddressPrefix: '*'
          destinationPortRange: '*'
          destinationAddressPrefix: '*'
        }
      }
    ]
  }
}

// Create Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2020-11-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: subnetName
        properties: {
          addressPrefix: '10.0.0.0/24'
          networkSecurityGroup: {
            id: nsg.id
          }
        }
      }
    ]
  }
}

// Create Public IP
resource publicIp 'Microsoft.Network/publicIPAddresses@2020-11-01' = {
  name: publicIpName
  location: location
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

// Create Network Interface
resource nic 'Microsoft.Network/networkInterfaces@2020-11-01' = {
  name: nicName
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          privateIPAllocationMethod: 'Static'
          privateIPAddress: '10.0.0.10'

          subnet: {
            id: vnet.properties.subnets[0].id
          }
          publicIPAddress: {
            id: publicIp.id
          }
        }
      }
    ]
  }
}

// Create Virtual Machine
resource vm 'Microsoft.Compute/virtualMachines@2020-12-01' = {
  name: vmName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    osProfile: {
      computerName: vmName
      adminUsername: adminUser
      adminPassword: vmPassword
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: nic.id
        }
      ]
    }
  }
}



// Create Public IP for Second VM
resource secondPublicIp 'Microsoft.Network/publicIPAddresses@2020-11-01' = {
  name: secondPublicIpName
  location: location
  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

// Create Network Interface for Second VM
resource secondNic 'Microsoft.Network/networkInterfaces@2020-11-01' = {
  name: secondNicName
  location: location
  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'
        properties: {
          privateIPAllocationMethod: 'Static'
          privateIPAddress: '10.0.0.11' // Changed IP

          subnet: {
            id: vnet.properties.subnets[0].id
          }
          publicIPAddress: {
            id: secondPublicIp.id
          }
        }
      }
    ]
  }
}

// Create Second Virtual Machine
resource secondVm 'Microsoft.Compute/virtualMachines@2020-12-01' = {
  name: secondVmName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B1s'
    }
    storageProfile: {
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    osProfile: {
      computerName: secondVmName
      adminUsername: adminUser
      adminPassword: vmPassword
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: secondNic.id
        }
      ]
    }
  }
}


output firstVmPublicIp string = publicIp.properties.ipAddress
output secondVmPublicIp string = secondPublicIp.properties.ipAddress
