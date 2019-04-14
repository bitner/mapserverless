# MapServerless AWS Lambda Layer

MapServerless is a perhaps useless, perhaps awesome way to run Mapserver in AWS Lambda. 

This example of how to deploy MapServer on AWS Lambda uses the Lambda Layer created with [https://github.com/bitner/mapserverless-layer]

Pull requests always welcome!


### Getting Started


To get started, you must have npm already installed on your system along with a couple plugins:
```sh
npm install -g serverless
serverless plugin install -n serverless-apigw-binary
serverless plugin install -n serverless-wsgi
```

From here, you can deploy using serverless:
```sh
serverless deploy
```

This command line will return information about what has been deployed. The most important bit here is the endpoints which will return a link like:
 ```
 endpoints:
    GET - https://udd8de3fz7.execute-api.us-west-1.amazonaws.com/dev/{proxy+}
```
Going to the link provided minus the {proxy+} will take you to an OpenLayers application set up to view the demo layers from natural earth (https://udd8de3fz7.execute-api.us-west-1.amazonaws.com/dev/) will remain up through FOSS4GNA as an example) 

The MapServer currently deployed is very basic and this deployment uses a couple natural earth layers that are included with the project. The data and a sample mapfile are currently stored with the lambda function. Future work could include making sure that the Lambda layer has further support for vsis3 and PostGIS to allow use of other layers. 
