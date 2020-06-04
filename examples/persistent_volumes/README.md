# Persistent Volumes 

- Read a bit of intro @ 
- Try hands on @ https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/
    - we we hostPath for creating a persistent volume here
    - if you are working on a multinode system, make sure that the pv-pod scheduled on the node you created 
    - refer to this: https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/ for learning to schedule the pod on a proper node
- Next step is to go into more indepth using https://kubernetes.io/docs/concepts/storage/persistent-volumes/
    - Here, we use local persistent volumes so that we don't have to schedule pods manually
    - first create a storage class
    - create a claim and pv
    - create pod

TODO: Use HELM for creating storage provisor
