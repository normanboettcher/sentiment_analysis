# 🚀 Red Hat OpenShift Local on Ubuntu (Developer Setup)

This guide walks you through setting up **Red Hat OpenShift Local** (formerly CodeReady Containers) on **Ubuntu Linux**
as an individual developer. It allows you to run a **single-node OpenShift cluster locally** for development and
testing.

---

## ✅ System Requirements

- **OS**: Ubuntu 20.04 or newer
- **CPU**: 4 vCPUs minimum
- **RAM**: 9 GB minimum (16 GB recommended)
- **Disk**: 35+ GB available
- **Virtualization**: Enabled in BIOS (Intel VT-x / AMD-V)

---

## 🔧 1. Install Dependencies

### Ubuntu

#### Install required packages for virtualization and networking:

```
sudo apt update
sudo apt install -y qemu-kvm libvirt-daemon libvirt-daemon-system libvirt-clients \
    bridge-utils virt-manager network-manager
```

#### Add your user to the `libvirt` group:

```
sudo usermod -a -G libvirt $(whoami)
newgrp libvirt
```

### Fedora/RHEL/CentOS

## 📦 2. Download OpenShift Local

1. Visit the OpenShift Local Downloads Page

2. Sign in or create a free Red Hat account

3. Download the OpenShift Local for Linux tarball

4. Extract and move the binary:

```
tar -xvf crc-linux-amd64.tar.xz
sudo mv crc-linux-amd64/ /usr/local/bin/
sudo ln -s /usr/local/bin/crc-linux-2.51.0-amd64/crc /usr/bin/crc
```

Or make your individual setup depending on your path settings :)

## 🔑 3. Get Your Pull Secret

Go to: https://console.redhat.com/openshift/create/local

1. Download the pull secret

2. Save it locally (e.g. as pull-secret.txt)

## ⚙️ 4. Set Up OpenShift Local

Run the following command to prepare your system for running OpenShift Local:

```
crc setup
```

The setup will take same time depending on your network speed.

## 🚀 5. Start the Cluster

Start OpenShift Local with:

```
crc start
```

## 🌐 6. Access OpenShift

### Web Console

Once the cluster is running, go to:

```
https://console-openshift-console.apps.crc.testing
```

#### Login credentials:

<b>Username</b>: developer

<b>Password</b>: developer

You can query your admin password via:

```
crc console --credentials
```

once the cluster is started.

### CLI Access (oc)

Set up your terminal to use the OpenShift CLI:

```
eval $(crc oc-env)
oc login -u developer -p developer https://api.crc.testing:6443
```

## 🌍 7. Understanding .crc.testing Domains

When you start the cluster, OpenShift Local sets up a local DNS configuration mapping:

- api.crc.testing → OpenShift API

- console-openshift-console.apps.crc.testing → Web Console

- *.apps.crc.testing → Routes for your apps

This is done by configuring dnsmasq and NetworkManager on your system.

You can test that DNS resolution works:

## Troubleshooting

If you get the following error on ubuntu:

```
INFO Creating CRC VM for OpenShift 4.18.2...      
INFO Generating new SSH key pair...               
INFO Generating new password for the kubeadmin user 
INFO Starting CRC VM for openshift 4.18.2...      
Error starting machine: Error in driver during machine start: virError(Code=9, Domain=10, Message='operation failed: Unable to find a satisfying virtiofsd')
```

Just use

```
sudo apt install virtiofsd
```

The error means libvirt is trying to use virtiofsd (a daemon used for file sharing between your host and the VM), but
it's not installed or not in the expected location