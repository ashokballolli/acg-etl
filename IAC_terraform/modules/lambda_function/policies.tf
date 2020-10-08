#
# AWS MANAGED POLICY
#
resource "aws_iam_role_policy_attachment" "aws-managed-policy-attachment01" {
  role = aws_iam_role.lambda_sns_role01.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "aws-managed-policy-attachment04" {
  role = aws_iam_role.lambda_sns_role01.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}
