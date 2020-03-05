# Play with stateless app

```bash
# build image 
docker build -t sedflix/flask_test ./app

# push image to a registery
docker push sedflix/flask_test

# now deploy the app
k apply -f deployment.yaml

# to increase the number of instances/replicas you can change it in the yaml and then apply it again

# rolling update
# set the new image and rolling update the image
kubectl set image deployments/hello-flask hello-flask=sedflix/flask_test
# get status of the rollout
kubectl rollout status deployments/hello-flask
# undo rollout
kubectl rollout undo deployments/hello-flask



# autoscaling 
# resource limits needs to be specified for this to work
# the metric server needs to be deployed and needs to be working  well
kubectl autoscale deployment hello-flask --min=1 --max=4
```