import * as cdk from 'aws-cdk-lib';
import * as path from 'path'
import { Construct } from 'constructs';
import { LambdaIntegration, RestApi } from 'aws-cdk-lib/aws-apigateway'
import { DockerImageCode, DockerImageFunction } from 'aws-cdk-lib/aws-lambda'
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class APIStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

      const testLambda = new DockerImageFunction(this, 'test-lambda', {
        code: DockerImageCode.fromImageAsset(path.join(__dirname, '../../helloWorldLambda')) 
      })

      const api = new RestApi(this, 'bank-data-pipeline-api');
      const test = api.root.addResource('test')
      test.addMethod('GET', new LambdaIntegration(testLambda))

  }
}
