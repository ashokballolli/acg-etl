provider "aws" {
  region = var.region
}
# aws_db_instance.rds-acg:
resource "aws_db_instance" "rds-acg-tf" {
  allocated_storage = var.max_allocated_storage
  auto_minor_version_upgrade = true
  availability_zone = var.availability_zone
  engine = var.engine
  engine_version = var.engine_version
  identifier = var.identifier
  instance_class = var.instance_class
  max_allocated_storage = 1000
  multi_az = var.multi_az
  port = var.port
  publicly_accessible = var.publicly_accessible
  skip_final_snapshot = true
  username = var.rds_username
  password = var.rds_password
  name = var.rds_database_name

  provisioner "local-exec" {
    command = "PGPASSWORD=${self.password} psql --host=${self.address} --port=${self.port} --username=${self.username} --dbname=${self.name} < ./schema.sql"
  }
}

# terraform plan -var-file="secret.tfvars"