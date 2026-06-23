output "public_ip" {
  value = aws_instance.devops_server.public_ip
}

output "ssh_command" {
  value = "ssh -i ubuntu-keypair.pem ubuntu@${aws_instance.devops_server.public_ip}"
}

output "jenkins_url" {
  value = "http://${aws_instance.devops_server.public_ip}:8080"
}

output "flask_url" {
  value = "http://${aws_instance.devops_server.public_ip}:5000"
}