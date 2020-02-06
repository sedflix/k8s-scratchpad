# k8s cluster setup

I've tried to follow [this blog](https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04) to setup a cluster using three systems.

## Step 1: Get Systems

- and install ansible on the local system.

## Step 2: initial.yml

```bash
    ansible-playbook -i hosts initial.yml
```

## Step 3: kube-dependcies.yml

```bash
    ansible-playbook -i hosts kube-dependcies.yml
```

TODO: setup firewall config

## Step 4: master.yml

```bash
    ansible-playbook -i hosts master.yml
```

In this step, `kubeadm init` task might take too long which might lead to failure of `copy` task. Therefore, you might need to do this seperately. (Not sure).


## 

```bash
kubectl drain ubuntu --delete-local-data --force --ignore-daemonsets
kubectl delete node ubuntu
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
sudo docker system prune
```

```bash

Aubuntu@ubuntu:~$ sudo swapoff -a
ubuntu@ubuntu:~$ sudo nano /etc/fstab
ubuntu@ubuntu:~$ sudo su -
root@ubuntu:~# cat > /etc/docker/daemon.json <<EOF
> {
>   "exec-opts": ["native.cgroupdriver=systemd"],
>   "log-driver": "json-file",
>   "log-opts": {
>     "max-size": "100m"
>   },
>   "storage-driver": "overlay2"
> }
> EOF
root@ubuntu:~# mkdir -p /etc/systemd/system/docker.service.d
root@ubuntu:~# systemctl daemon-reload
root@ubuntu:~# systemctl restart docker
root@ubuntu:~# systemctl restart docker

```


https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/
https://docs.vmware.com/en/VMware-vSphere/6.7/Cloud-Native-Storage/GUID-60892633-B826-4CF4-B75B-D5360C847C71.html
https://medium.com/better-programming/build-your-own-multi-node-kubernetes-cluster-with-monitoring-346a7e2ef6e2