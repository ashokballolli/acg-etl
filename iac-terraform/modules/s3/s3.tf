provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "backup" {
  bucket = var.bucket
  acl = var.acl
}
