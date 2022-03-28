# Kubenetes-Simple-Project
In an Kubernetes cluster, add a simple new web service that runs inside the cluster. The service should only be routable from outside the cluster on the URL `http://local.magneto.org/handbag` (for example). This endpoint should only accept GET requests on this exact path. In this case, it should return a JSON response informing us of your favourite hand-bag. This service should be maintained under source control, and should be tested and deployed to the Kubernetes cluster via CI/CD. For example, if we modified the service’s code to also
allow PUT requests, this change should be validated and automatically rolled out to the cluster after the change has been merged to the mainline branch.

# Tips -
When designing the solution you may choose to make any simplifying assumptions that you believe make sense for the task, but please make note of these where appropriate. When writing the code and configuration, treat it as something to run in a production system - thus, considering practices around reproducibility, scalability, and observability. However, detailed implementation of these areas are not required! If the solution needs
additional work before it is suitable for production, or there are future extensions which you think are important but not critical, please briefly document them.

# Technologies ( These are technologies can be used ) :
● Primary languages for backend service Python.
● For dependency management, may be Flask for Python.
● For infrastructure management, Terraform and a small amount of bash or
Python scripting where necessary.
● GitHub for source control, and both GitHub Actions and Jenkins for CI/CD.
● To run Kubernetes clusters use EKS, AWS’s managed Kubernetes service.
● For Kubernetes services management, use Helm for infrastructure and third-party
services, and a small internal jsonnet library for internally-developed applications.
● For Kubernetes ingress, use both AWS ALBs and the ingress-nginx controller.

=====