pipeline {
  agent any

  environment {
    REGISTRY_URL = '352708296901.dkr.ecr.us-west-2.amazonaws.com'
    ECR_REGION = 'us-west-2'
    K8S_NAMESPACE = 'adham-namespace'
    K8S_CLUSTER_NAME = 'devops-alfnar-k8s'
    K8S_CLUSTER_REGION = 'eu-north-1'
  }

  stages {

    stage('Creating NAMESPACE'){
      steps{
         sh '''
         aws eks --region ${K8S_CLUSTER_REGION} update-kubeconfig --name ${K8S_CLUSTER_NAME}
         kubectl create namespace ${K8S_NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
         '''
      }
    }

    stage('MNIST Web Server - build'){
      when { branch "master" }
      steps {
          sh '''
          image_web="mnist-webserver:0.0.${BUILD_NUMBER}"
          cd webserver
          aws ecr get-login-password --region $ECR_REGION | docker login --username AWS --password-stdin ${REGISTRY_URL}
          docker build -t ${image_web} .
          docker tag ${image_web} ${REGISTRY_URL}/${image_web}
          docker push ${REGISTRY_URL}/${image_web}
          '''
      }
    }

    stage('MNIST Web Server - deploy'){
        when { branch "master" }
        steps {
            sh '''
            cd infra/k8s
            image_web_name= "mnist-webserver:0.0.${BUILD_NUMBER}"
            # replace registry url and image name placeholders in yaml
            sed -i "s/{{REGISTRY_URL}}/$REGISTRY_URL/g" mnist-predictor.yaml
            sed -i "s/{{K8S_NAMESPACE}}/$K8S_NAMESPACE/g" mnist-predictor.yaml
            sed -i "s/{{IMG_NAME}}/$image_web_name/g" mnist-predictor.yaml

            # get kubeconfig creds
            aws eks --region ${K8S_CLUSTER_REGION} update-kubeconfig --name ${K8S_CLUSTER_NAME}

            # apply to your namespace
            kubectl apply -f mnist-predictor.yaml -n $K8S_NAMESPACE
            '''
        }
    }


    stage('MNIST Predictor - build'){
        when { branch "master" }
        steps {
            sh '''
            IMAGE="mnist-predictor:0.0.${BUILD_NUMBER}"

            cd ml_model
            aws ecr get-login-password --region $ECR_REGION | docker login --username AWS --password-stdin ${REGISTRY_URL}
            docker build -t ${IMAGE} .
            docker tag ${IMAGE} ${REGISTRY_URL}/${IMAGE}
            docker push ${REGISTRY_URL}/${IMAGE}
            '''
        }
    }

    stage('MNIST Predictor - deploy'){
        when { branch "master" }
        steps {
            sh '''
            cd infra/k8s
            IMG_NAME=mnist-predictor:0.0.${BUILD_NUMBER}

            # replace registry url and image name placeholders in yaml
            sed -i "s/{{REGISTRY_URL}}/$REGISTRY_URL/g" mnist-predictor.yaml
            sed -i "s/{{K8S_NAMESPACE}}/$K8S_NAMESPACE/g" mnist-predictor.yaml
            sed -i "s/{{IMG_NAME}}/$IMG_NAME/g" mnist-predictor.yaml

            # get kubeconfig creds
            aws eks --region ${K8S_CLUSTER_REGION} update-kubeconfig --name ${K8S_CLUSTER_NAME}

            # apply to your namespace
            kubectl apply -f mnist-predictor.yaml -n $K8S_NAMESPACE
            '''
        }
    }
  }
}


