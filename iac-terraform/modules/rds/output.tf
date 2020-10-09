output "rds_hostname" {
  value = aws_db_instance.rds-acg-tf.address
}
output "rds_port" {
  value = aws_db_instance.rds-acg-tf.port
}
output "rds_db_name" {
  value = aws_db_instance.rds-acg-tf.name
}
output "rds_db_username" {
  value = aws_db_instance.rds-acg-tf.username
}
output "rds_db_password" {
  value = aws_db_instance.rds-acg-tf.password
}
