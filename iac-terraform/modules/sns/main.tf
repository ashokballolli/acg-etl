terraform {
  required_version = ">= 0.13.4"
}

provider "aws" {
  region = var.region
}

data "template_file" "cloudformation_sns_stack" {
  template = file("${path.module}/templates/email-sns-stack.json.tpl")

  vars = {
    display_name = var.display_name
    subscriptions = join(
      ",",
      formatlist(
        "{ \"Endpoint\": \"%s\", \"Protocol\": \"%s\"  }",
        var.email_addresses,
        var.protocol,
      ),
    )
    topic_name = var.sns_topic_name
  }
}

resource "aws_cloudformation_stack" "sns_topic" {
  name          = var.stack_name
  template_body = data.template_file.cloudformation_sns_stack.rendered
}

