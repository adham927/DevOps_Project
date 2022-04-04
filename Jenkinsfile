pipeline {
  agent any

  environment {
    REGISTRY_URL = '352708296901.dkr.ecr.us-west-2.amazonaws.com/web_server_adham'
    ECR_REGION = 'us-west-2'
    K8S_NAMESPACE = 'adham-namespace'
  }

  stages {

    stage('Creating NAMESPACE'){
      steps{
         sh '''
         aws eks --region eu-north-1 update-kubeconfig --name devops-alfnar-k8s
         NS=$(kubectl get namespace ${K8S_NAMESPACE} --ignore-not-found);
         if [[ "$NS" ]]; then
            echo "Skipping creation of namespace ${K8S_NAMESPACE} - already exists";
         else
            echo "Creating namespace ${K8S_NAMESPACE};
            kubectl create namespace ${K8S_NAMESPACE}
         fi;
         '''
      }
    }

    stage('MNIST Web Server - build'){
      when { branch "master" }
      steps {
          sh '''
          echo building
          '''
      }
    }

    stage('MNIST Web Server - deploy'){
        when { branch "master" }
        steps {
            sh '''
            echo deploying
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
            aws eks --region eu-north-1 update-kubeconfig --name devops-alfnar-k8s

            # apply to your namespace
            kubectl apply -f mnist-predictor.yaml -n $K8S_NAMESPACE
            '''
        }
    }
  }
}


