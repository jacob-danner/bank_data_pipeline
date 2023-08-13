import * as cdk from 'aws-cdk-lib';
import * as path from 'path'
import { Construct } from 'constructs';
import { LambdaIntegration, RestApi } from 'aws-cdk-lib/aws-apigateway'
import { DockerImageCode, DockerImageFunction } from 'aws-cdk-lib/aws-lambda'

export class APIStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

      const quarterDataCollectorLambda = new DockerImageFunction(this, 'quarter_data_collector', {
        code: DockerImageCode.fromImageAsset(path.join(__dirname, '../../lambdas/quarter_data_collector')) 
      })

      const quarterRequestGeneratorLambda = new DockerImageFunction(this, 'quarter_request_generator', {
        code: DockerImageCode.fromImageAsset(path.join(__dirname, '../../lambdas/quarter_request_generator')),
        environment: {
          "QUARTER_DATA_COLLECTOR_ARN": quarterDataCollectorLambda.functionArn
        }
      })

      quarterDataCollectorLambda.grantInvoke(quarterRequestGeneratorLambda) // allow request generator to invoke data collector

      const api = new RestApi(this, 'bank-data-pipeline-api');
      const trigger = api.root.addResource('trigger')
      trigger.addResource('quarter_request_generator').addMethod('POST', new LambdaIntegration(quarterRequestGeneratorLambda))


  }
}
