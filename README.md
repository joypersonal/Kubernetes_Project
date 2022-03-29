# Kubernetes Assignments and Solution:

# Overview

The purpose of this exercise is for us to gain some insight into how you approach the design,
documentation, and automation of common cloud infrastructure, as well as your basic coding
skills and familiarity with web service environments. While we will mention specific
technologies that are already in use at Ecosia, in each case you are free to use whatever
you are comfortable with. We also provide some information on principles that guide how the
Platform (SRE) team is currently working. Please read the entire assignment before starting.
Specification
Given an existing Kubernetes cluster, we want to add a simple new web service that runs
inside the cluster. The service should only be routable from outside the cluster on the URL
`http://local.ecosia.org/tree`. This endpoint should only accept GET requests on this exact
path. In this case, it should return a JSON response informing us of your favourite tree.
This service should be maintained under source control and should be tested and deployed
to the Kubernetes cluster via CI/CD. For example, if we modified the service’s code to also
allow PUT requests, this change should be validated and automatically rolled out to the
cluster after the change has been merged to the mainline branch.

# Tips

When designing your solution, you may choose to make any simplifying assumptions that
you believe make sense for the task, but please make note of these where appropriate.
When writing your code and configuration, treat it as something to run in a production
system - thus, considering practices around reproducibility, scalability, and observability.
However, we do not expect a detailed implementation of these areas! If you think that your
solution needs additional work before it is suitable for production, or there are future
extensions that you think are important but not critical, please briefly document them.
The upcoming stages of our interview process may ask you to extend your solution in
collaboration with an SRE on the Platform team. We may also ask you to present and
explain your approach to other stakeholders in the engineering organization.

# Technologies

Here is some information on the technologies we use at Ecosia. Choosing some of these
may make it easier for us to review or validate your solution, but using them is not required:
you can use whatever tools and languages that you are most comfortable with and which
you think are suitable for the task. However, bear in mind that if you choose an uncommon
technology, we would hope to see an explanation of your reasoning behind the choice.

● Our primary languages for backend services are Python, Go, and Node.js.
● For dependency management, we typically use Poetry for Python, yarn for Node.js,
and Go’s built-in modules support.
● For infrastructure management, we use Terraform and a small amount of bash or
Python scripting where necessary.
● We use GitHub for source control, and both GitHub Actions and CircleCI for CI/CD.
● To run Kubernetes clusters, we use EKS, AWS’s managed Kubernetes service. We
also use minikube in some circumstances for local testing.
● For Kubernetes services management, we use Helm for infrastructure and third-party
services, and a small internal jsonnet library for internally-developed applications.
● For Kubernetes ingress, we use both AWS ALBs and the ingress-nginx controller.

# Guiding Principles

The Platform team at Ecosia has agreed upon a set of seven principles that we use to
capture our shared vision and guide us in our day-to-day decision-making. Here are three
which we think are relevant to this assignment and which may help guide your process:
1. Choose simplicity. We avoid unnecessary complexity and operate the minimal
possible set of systems. We prefer to leverage and re-use existing systems rather
than innovation for innovation’s sake.
2. Deeply understand our evolving systems. Knowing our platform inside and out
helps with operational excellence. This understanding also allows us to provide a
better experience to our customers. We prize knowledge sharing and documentation,
and we make time for them.
3. Automation is better than repetition. Our code always shows the truth. We believe
strongly in the power of automation to facilitate standardization, reproducibility, and
understandability. We keep manual intervention to an absolute minimum.
---------------------------------------------------------------------------

# Step-by-step Solution

1. Setup an AWS EC2 Instance 
        
      The first step would be for us to set up an EC2 instance and on this instance, we will be  
      installing –

        1. JDK 
        2. Jenkins 
        3. eksctl 
        4. kubectl

1.1	Launch EC2 instance

       But first, let's head over to AWS, and in the search box type in ec2. 

       AWS EC2 setup 
       Click on the EC2 and after that, you need to look for the Launch Instance option - 

       AWS EC2 Launch Instance 
       Now select the image type for the EC2 instance (For this project we are going to select Ubuntu 
       Server 20.04) 

       AWS EC2 Launch Instance 
       Choose an Instance Type. 

       For this project, we are going to use t2.medium because we will be installing Jenkins and  
       t2.micro will not be sufficient enough to set up Jenkins AWS EC2 Choose instance type 
       Configure Instance Details - you can simply verify the detail and proceed to add the storage 
       part. 

       AWS EC2 configure instance details 
       Add storage - In general 8 Gib of memory is sufficient enough for setting up Jenkins 

       AWS EC2 add storage 
       Add tags - This part is optional but you can add some meaningful tag names to your EC2 
       instance. 

       AWS EC2 add tags 
       Configure Security group - This is an important step because here we need to add Custom  
       TCP port 8080, if you do not add this port then you will not be able to access Jenkins using  
       the public IP address of the AWS EC2 instance. 
       AWS EC2 add security group 
       Finally, click on review and launch 

       But before you launch your EC2 instance you need to create and download the key 
       pair (private key and public key) 

      AWS EC2 create a new key pair 
      Type in the key pair name and then click on the Download Key Pair. 
      AWS EC2 create a new key pair and download key 
      Your ec2 instance should be up and running.

2. Connect to EC2 Instance 

      Before you connect to your EC2 instance you must start EC2 instance. 
      Goto your AWS EC2 dashboard and click on EC2 after that click on Instances(running). 
      Remove the running filter and you should see your EC2 instance which you set up in Step 1. 
      Connect AWS EC2 
      Now we need to start the EC2 instance and it can be done by first selecting the instance and   
      then 
      Goto-> Instance Start -> Start Instance 
      Once the instance state is Running you can select the instance and click on Connect 

      We will connect using SSH Client - 
      AWS EC2 Connect to instance SSH Client 
      We will use the joy.pem file to connect, so carefully copy the ssh command. (Following    
      the command will be different for you because the IP address of EC2 instance will always be    
      different for you and also you need to supply your server pem file)
 
      ssh -i "joy.pem" ubuntu@ec2-34-238-83-117.compute-1.amazonaws.com 

      After successful login, you should see something similar on your terminal - 
      SSH into AWS ec2 instance using pem file




3. Install JDK on AWS EC2 Instance
 
     The next requirement is we need to install JAVA(JDK) on the EC2 instance. 
     In the previous step, we have seen how to connect and ssh into the EC2 instance. 
     Now before we do the JDK installation let's first update the package manager of the virtual  
     machine –

     sudo apt-get update 

     Check if you have java already installed onto your EC2 machine by running the following  
     command –

     java -version

     In case if you do not have java installed then you will see the following message - 
     Command 'java' not found, but can be installed with:

     sudo apt install openjdk-11-jre-headless # version 11.0.11+9-0ubuntu2~20.04, or 
     sudo apt install default-jre # version 2:1.11-72 
     sudo apt install openjdk-13-jre-headless # version 13.0.7+5-0ubuntu1~20.04 
     sudo apt install openjdk-16-jre-headless # version 16.0.1+9-1~20.04 
     sudo apt install openjdk-8-jre-headless # version 8u292-b10-0ubuntu1~20.04 
     sudo apt install openjdk-14-jre-headless # version 14.0.2+12-1~20.04 

     But you can install java by running the following command -
     
     sudo apt install openjdk-11-jre-headless 

     If you see the following message then you have installed java successfully - 
     openjdk version "11.0.11" 2021-04-20

     OpenJDK Runtime Environment (build 11.0.11+9-Ubuntu-0ubuntu2.20.04) 
     OpenJDK 64-Bit Server VM (build 11.0.11+9-Ubuntu-0ubuntu2.20.04, mixed mode, sharing) 

4. Install and Setup Jenkins
 
     The next step would be to install the Jenkins. You can follow the official Jenkins Installation   
     guide also. But here I have listed down the steps for installing the Jenkins on the EC2 instance. 
     First, we need to add the Jenkins repository to the package manager –
 
     wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add - 
     sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ >   
     /etc/apt/sources.list.d/jenkins.list'

    After adding the repository link of Jenkins update the package manager

    sudo apt-get update 

    Then finally install Jenkins using the following command 

    sudo apt-get install jenkins 

    On successful installation, you should see Active Status
 
    sudo service jenkins status
 
    ● _jenkins.service - LSB: Start Jenkins at boot time 
    Loaded: loaded (/etc/init.d/jenkins; generated) 
    Active: active (exited) since Tue 2021-06-22 20:31:18 UTC; 37s ago 
    Docs: man:systemd-sysv-generator(8) 
    Process: 16297 ExecStart=/etc/init.d/jenkins start (code=exited, status=0/SUCCESS) 

 4.1 Setup Jenkins
 
    After installing jenkins lets go back to AWS dashboard -> EC2 -> Instances(running) 
    AWS EC2 click on instance ID for public IP address 
    Click on the instance ID as mentioned in the above image. 
    Now we need to find the public IP address of the EC2 machine so that we can access the   
    Jenkins. 
    Once you click on the instance ID you should see the following page with lots of information  
    about the EC2 instance. 
    We need to look for a public IPv4 address 
    AWS EC2 click on instance ID for public IP address 
    Alright now we know the public IP address of the EC2 machine, so now we can access the    
    Jenkins from the browser using the public IP address followed by the port 8080 
    Jenkins access url after installing

    If you are installing the Jenkins for the first time then you need to supply the       
    initialAdminPassword and you can obtain it from –

    sudo cat /var/lib/jenkins/secrets/initialAdminPassword 

    Copy the password and paste it into the initial page of the Jenkins. After that, Jenkins will 
    prompt you for installing the plugins. 
    Opt for installing the suggested plugin - 
    Jenkins install suggested plugins 
    After completing the installation of the suggested plugin you need to set the First Admin User     
    for Jenkins Jenkins set the first admin user 
    Also, check the instance configuration because it will be used for accessing the Jenkins 
    jenkins instance configuration and now your Jenkins is ready for use 

5. Update visudo and assign administrative privileges to jenkins  
    user 

     Now we have installed the Jenkins on the EC2 instance. To interact with the Kubernetes  
     cluster Jenkins will be executing the shell script with the Jenkins user, so the Jenkins user   
     should have an administration(superuser) role assigned forehand. 
     Let’s add jenkins user as an administrator and also ass NOPASSWD so that during the    
     pipeline run it will not ask for a root password. 
     Open the file /etc/sudoers in vi mode
 
     sudo vi /etc/sudoers

     Add the following line at the end of the file 
     jenkins ALL=(ALL) NOPASSWD: ALL 

    After adding the line save and quit the file. 
    Now we can use Jenkins as root user and for that run the following command –

    sudo su - jenkins 

6. Install Docker

    Now we need to install the docker after installing the Jenkins. 
    The docker installation will be done by the Jenkins user because now it has root user    
    privileges. 
    Use the following command for installing the docker - 

    sudo apt install docker.io 

    After installing the docker you can verify it by simply typing the docker --version onto the 
    terminal 
    It should return you with the latest version of the docker 
    Docker version 20.10.2, build 20.10.2-0ubuntu1~20.04.2 
 
6.1 Add jenkins user to Docker group
 
   Jenkins will be accessing the Docker for building the application Docker images, so we need to   
   add the Jenkins user to the docker group. 

   sudo usermod -aG docker Jenkins

7. Install and Setup AWS CLI

   Okay so now we have our EC2 machine and Jenkins installed. Now we need to set up the AWS   
   CLI on the EC2 machine so that we can use eksctl in the later stages 
   Let us get the installation done for AWS CLI
 
   sudo apt install awscli 
 
   Verify your AWS CLI installation by running the following command - 

   aws –version

   It should return you with the version of CLI 
   aws-cli/1.18.69 Python/3.8.5 Linux/5.4.0-1045-aws botocore/1.16.19

7.1 Configure AWS CLI

   Okay now after installing the AWS CLI, let’s configure the AWS CLI so that it can authenticate    
   and communicate with the AWS environment. 

   To configure the AWS the first command we are going to run is - 

   aws configure 

   Once you execute the above command it will ask for the following information - 
   1. AWS Access Key ID [None]: 
   2. AWS Secret Access Key [None]: 
   3. Default region name [None]: 
   4. Default output format [None]: 

   You can find this information by going into AWS -> My Security Credentials 
   AWS EC2 my security credentials for AWS CLI 
   Then navigate to Access Keys (access key ID and secret access key) 
   AWS EC2 access keys for setting up AWS CLI 
   You can click on the Create New Access Key and it will let you generate - AWS Access Key ID,     
   AWS Secret Access Key. 
   AWS EC2 download access key id and secret access key for aws configure 
  (Note: - Always remember you can only download your access id and secret once if you    
  misplace the secret and access then you need to recreate the keys again) 

   Default region name - You can find it in the menu 
   AWS EC2 region for AWS CLI Default region-name 
   Alright, now we have installed and set up AWS CLI.

8. Install and Setup Kubectl

   Moving forward now we need to set up the kubectl also onto the EC2 instance where we set up    
   the Jenkins in the previous steps. 
   Here is the command for installing kubectl 
   
   curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s   
   https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" 
   chmod +x ./kubectl 
   sudo mv ./kubectl /usr/local/bin 
 
   Verify the kubectl installation 
   Verify the kubectl installation by running the command kubectl version and you should see the   
   following output 
   Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.2",    
   GitCommit:"092fbfbf53427de67cac1e9fa54aaa09a28371d7", GitTreeState:"clean",  
   BuildDate:"2021-06-16T12:59:11Z", GoVersion:"go1.16.5", Compiler:"gc",  
   Platform:"linux/amd64"} 
   Error from server (Forbidden): <html><head><meta http-equiv='refresh'  
 content='1;url=/login?from=%2Fversion%3Ftimeout%3D32s'/><script>window.location.replace('/lo 
   gin?from=%2Fversion%3Ftimeout%3D32s');</script></head><body style='background-
   color:white; color:white;'>

9. Install and Setup eksctl

   The next thing which we are going to install the eksctl, which we will be used to create    
   AWS EKS Clusters. 
   Okay, the first command which we are gonna run to install the eksctl

   curl --silent –location   
   "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -
   s)_amd64.tar.gz" | tar xz -C /tmp 

   sudo mv /tmp/eksctl /usr/local/bin 

   Verify the installation by running the command –

   eksctl version

   And it will return you with the version - 
   0.52.0 
   So, at the time of installation, I had 0.52.0


10. Create eks cluster using eksctl
 
    In all the previous 9 steps we were preparing our AWS environment. Now in this step, we are   
    going to create EKS cluster using eksctl 
    You need the following in order to run the eksctl command

    1. Name of the cluster: –name flaskapp-cluster
    2. Version of Kubernetes: –version 1.17 
    3. Region: –name us-west-1
    4. Nodegroup name/worker nodes: worker-nodes 
    5. Node Typ: t2.micro 
    6. Number of nodes: -nodes 2 

    Here is the eksctl command –

    eksctl create cluster --name flaskapp-cluster --version 1.17 --region us-west-1 --nodegroup-   
    name worker-nodes --node-type t2.micro --nodes 2
    (*Note - Be patient with the above command because it may take 20-30 minutes to complete) 
    For me it almost took 20 minutes, here are the timestamps


10.1 Verify the EKS kubernetes cluster from AWS 

    You can go back to your AWS dashboard and look for Elastic Kubernetes Service -> Clusters 
    use eksctl to setup AWS EKS cluster 
    Click on the Cluster Name to verify the worker nodes –

    eksc nodes

11. Add Docker and GitHub Credentials into Jenkins 

11.1 Setup Docker Hub Secret Text in Jenkins

   You can set the docker credentials by going into - 
   Goto -> Jenkins -> Manage Jenkins -> Manage Credentials -> Stored scoped to jenkins ->   
   global -> Add Credentials 
   Jenkins add credentials as secret text for docker
 
11.2 Setup GitHub Username and password into Jenkins

   Now we add one more username and password for GitHub. 
   Goto -> Jenkins -> Manage Jenkins -> Manage Credentials -> Stored scoped to jenkins ->    
   global -> Add Credentials

12. Add Jenkins stages

node {

    stage("Git Clone"){

        git credentialsId: 'GIT_HUB_CREDENTIALS', url: 'https://github.com/joypersonal/Kubernetes_Project'
    }

    stage("Docker build"){
        sh 'sudo docker version'
        sh 'sudo docker build -t joysarkar81/webapp:v4 .'
        sh 'sudo docker image list'
        
    }

    withCredentials([string(credentialsId: 'DOCKER_HUB_PASSWORD', variable: 'PASSWORD')]) {
        sh 'docker login -u joysarkar81 -p $PASSWORD'
    }

    stage("Push Image to Docker Hub"){
        sh 'docker push  joysarkar81/webapp:v4'
    }
    
    stage("kubernetes deployment"){
        sh 'kubectl delete deployment webapp'
        sh 'kubectl apply -f kubernetes/deployment.yml'
		sh 'kubectl apply -f kubernetes/service.yml'
    }
}

13. Build, deploy and test CI/CD pipeline

   Create a new Pipeline: Goto Jenkins Dashboard or Jenkins home page click on New Item 
    Jenkins new item for creating the pipeline 
   Pipeline Name: Now enter Jenkins pipeline name and select Pipeline 
    Enter an item name for jenkins pipeline 
   Add pipeline script: Goto -> Configure and then pipeline section. 
   Copy the Jenkins script from Step 12 and paste it there. 
   Build and Run Pipeline: Now goto pipeline and click on build now 
  
  Verify using kubectl commands 
   Run the below commands: 
   aws configure 
   (region, secrete key and access key) 
   aws eks --region us-west-1 update-kubeconfig --name flaskapp-cluster

   output: Added new context arn:aws:eks:us-west-1:404622708094:cluster/flaskapp-cluster to 
   /Users/joy/.kube/config

   You can also verify the Kubernetes deployment and service with kubectl command. e.g kubectl  
  get deployments, kubectl get service

  Kubectl deployment status check after deploying application on AWS
 
    Kubectl service status check after deploying application on AWS


joy@FVFDC5NGM6KJ certs % kubectl get deployments
NAME     READY   UP-TO-DATE   AVAILABLE   AGE
webapp   2/3     3            2           22m

joy@FVFDC5NGM6KJ Kubernetes_Project % kubectl get service
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes    ClusterIP   10.100.0.1      <none>        443/TCP        2d13h
web-service   NodePort    10.100.152.90   <none>        80:30833/TCP   2d11h

joy@FVFDC5NGM6KJ certs % kubectl get pods
NAME                      READY   STATUS    RESTARTS   AGE
webapp-55cb949f78-4pvp9   1/1     Running   0          25m
webapp-55cb949f78-bkdnp   0/1     Pending   0          25m
webapp-55cb949f78-rwn96   1/1     Running   0          25m

Also, run the python code locally and check everything is working fine.


  
 


 
                                     
You can access the rest end point from browser using the EXTERNAL-IP address
However, need to create and expose LoadBalancer service. Use the below command from Jenkins server -

jenkins@ip-172-31-84-68:~$ kubectl expose deployment webapp --type LoadBalancer --name app-service-lb
service/app-service-lb exposed

jenkins@ip-172-31-84-68:~$ kubectl get services
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)          AGE
app-service-lb   LoadBalancer   10.100.174.47   a63895b75a8794b20bb1e7bd45adefc3-1557322788.us-west-1.elb.amazonaws.com   5000:31400/TCP   86m
kubernetes       ClusterIP      10.100.0.1      <none>                                                                    443/TCP          2d21h
web-service      NodePort       10.100.152.90   <none>                                                                    80:30833/TCP     2d19h

Hence the service URL would be –

a63895b75a8794b20bb1e7bd45adefc3-1557322788.us-west-1.elb.amazonaws.com:5000/tree


 


                               ----------------x----------x---------x-----------x----------------
   	

