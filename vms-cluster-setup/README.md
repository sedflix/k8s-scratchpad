# k8s cluster setup

I've tried to follow [this blog](https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04) to setup a cluster using three systems.
[This link](https://docs.vmware.com/en/VMware-vSphere/6.7/Cloud-Native-Storage/GUID-60892633-B826-4CF4-B75B-D5360C847C71.html) a pretty cool guide for setting up a cluster using VMS

## Step 1: Get Systems 

- We got one master node and two worker nodes.
- Make sure names of nodes are unique
- Turn the swap off
- Use systemd for controlling docker(idk why or if it is important)
- and install ansible on the local system

How to turn off swap manually?
```bash

ubuntu@ubuntu:~$ sudo swapoff -a
ubuntu@ubuntu:~$ sudo nano /etc/fstab 
ubuntu@ubuntu:~$ sudo su -
```

How to use systemd for controlling docker?
```bash

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


### Mye need commands

Messsed your installation? Reset it using the following
```bash
kubectl drain ubuntu --delete-local-data --force --ignore-daemonsets
kubectl delete node ubuntu
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X
sudo rm -rf /etc/cni/net.d/
sudo rm -rf /var/lib/cni
sudo docker system prune
```




https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/
https://medium.com/better-programming/build-your-own-multi-node-kubernetes-cluster-with-monitoring-346a7e2ef6e2

## Accessing cluster externally 

* Start Proxy: `k proxy --address='0.0.0.0' --accept-hosts='^192.168.*.*$'`
* Copy content of `kubectl config view --raw`
* Replace the port number in `server: https://192.168.1.206:6443` with the port the proxy is running
* Paste the content in `~/.kube/config`
* Have fun!

Proxy enables non-HTTPs and access without the requirement of access-tokens and weird cetificates.

## Setting Up k8s dashboard

When using RBAC, kubeconfig Authentication method does not support external identity providers or certificate-based authentication. And kubectl proxy doesn't seem to work (IDK why it doesn't reply back).
So we are using this particular method.

### Step 1: Deploy k8s-dashboard
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-rc3/aio/deploy/recommended.yaml

```

### Step 2: Edit kubernetes-dashboard service

We need to edit dashboard service and change service “type” from ClusterIP to NodePort.

```bash
kubectl -n kubernetes-dashboard edit service kubernetes-dashboard
```

### Step 3: See the assigned port number

```bash
sid) kubectl -n kubernetes-dashboard get services
NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
dashboard-metrics-scraper   ClusterIP   10.103.105.97   <none>        8000/TCP        28d
kubernetes-dashboard        NodePort    10.104.141.42   <none>        443:30251/TCP   28d
```

### Step 4: Get access token
```bash
sid) kubectl -n kube-system describe $(kubectl -n kube-system get secret -n kube-system -o name | grep namespace) 
Name:         namespace-controller-token-jhn6t
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: namespace-controller
              kubernetes.io/service-account.uid: 720fa91c-746b-4542-bb1c-01162375506b

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6Il9qTTlmd3IxNXJ1Rmkycy1JSUt4RDNLdWVtUmx2cGpWNTM3dXlCMmF6N0EifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlci10b2tlbi1qaG42dCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuYW1lc3BhY2UtY29udHJvbGxlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjcyMGZhOTFjLTc0NmItNDU0Mi1iYjFjLTAxMTYyMzc1NTA2YiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpuYW1lc3BhY2UtY29udHJvbGxlciJ9.jJAJexPRAOX3oYupD1T8qcgK3zVqKxTsMI6V84jUaHibrE07r2kKroFB7e-Kjj5eehQPQsAbnjRdhJi5cXR2zziBk39InaSmYcj2AUEFv1XL7Q92S209U07eYj4Ut4jcqmGFdf991RdHpMOBGIIXWuwriI_OYFxBCsA0x-trM44dmwf802dxV0CAfZndmnCIFTS1yM8G05vsVZ3F6Z7oSsGk_JMC8MHAT3DIdjQhnUOiMISk5nAVOP0aDJXfp2dIJwzm_bJS5x4JdgkpmT7q3yqlav353kHJCIoR8cUp5mFAi2tw81P1SoLYW4tNR4oZsUJWZVUFMNhNnJBJ-pvrXw
```

### Voila 

Access your dashboard at http://master_node_ip:port, here it will be http://192.168.1.206:30251/. 
Since this is insecure, Google Chrome won't allow you to access this URL. Tick: type the text "badidea" and "thisisunsafe" on the warning screening and press enter.
