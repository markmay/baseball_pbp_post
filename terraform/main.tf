terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-2"
}

module "stat_pbp_lambda" {
  source             = "git::https://github.com/terraform-aws-modules/terraform-aws-lambda.git?ref=4cf383ea0b3d71c0c044326f69e1827f0d114ea9"
  function_name      = "stat_pbp_x_poster"
  description        = "Baseball Play By Play Parse/Poster"
  handler            = "stat_x_pbp_bot.handler"
  runtime            = "python3.10"
  timeout            = 10
  memory_size        = 128
  publish            = true
  attach_policies    = true
  policies           = [aws_iam_policy.stat_pbp_secrets_policy.arn]
  number_of_policies = 1

  source_path = [
    "${path.module}/../src/",
    {
      pip_requirements = "${path.module}/../src/requirements.txt"
    }
  ]
}

resource "aws_iam_policy" "stat_pbp_secrets_policy" {
  name = "stat_pbp_secrets_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = ["*"]
      }
    ]
  })
}


module "pbp_x_orchestrator_stepfunction" {
  source    = "git::https://github.com/terraform-aws-modules/terraform-aws-step-functions.git?ref=14d513560d56c2876982bc687c98e4cb6ec3bc17"
  name      = "pbp_x_orchestrator"
  role_name = "pbp_x_orchestrator_sf_role"
  logging_configuration = {
    include_execution_data = true
    level                  = "ALL"
  }
  definition = templatefile("${path.module}/pbp_x_orchestrator_stepfunction.json", {
    stat_pbp_lambda_arn = module.stat_pbp_lambda.lambda_function_arn
  })
  type               = "STANDARD"
  attach_policies    = true
  number_of_policies = 1
  policies = [
    aws_iam_policy.pbp_x_orchestrator_sf_role_invoke_lambdas.arn
  ]
}

resource "aws_iam_policy" "pbp_x_orchestrator_sf_role_invoke_lambdas" {
  name = "pbp_x_orchestrator_sf_role_invoke_lambdas"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["lambda:InvokeFunction"]
        Resource = [
          module.stat_pbp_lambda.lambda_function_arn
        ]
      }
    ]
  })
}
