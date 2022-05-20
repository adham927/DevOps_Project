terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}


resource "aws_instance" "app_server" {
  ami           = "ami-0341aeea105412b57"
  instance_type = "t3a.large"
  key_name = "adham-keypair"
  tags = {
    Name = var.ec2_name
  }
  provisioner "remote-exec"  {
    inline  = [
      "sudo yum update –y",
      "sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo",
      "sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key",
      "sudo yum upgrade",
      "sudo amazon-linux-extras install java-openjdk11 -y",
      "sudo yum install jenkins -y",
      "sudo systemctl enable jenkins",
      "sudo systemctl start jenkins",
      "sudo amazon-linux-extras install epel -y",
      "sudo yum install git -y",
      "sudo yum install docker",
      "sudo usermod -a -G docker jenkins",
      "sudo systemctl enable docker.service",
      "sudo systemctl enable containerd.service",
      "sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo",
      "sudo yum -y install terraform"
      ]
   }
  connection {
    type         = "ssh"
    host         = self.public_ip
    user         = "ec2-user"
    timeout = "7m"
    private_key  = file("C:/Users/adham-keypair.pem")
   }
}




