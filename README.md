## ECS CLI V2 Sample App

The ECS CLI is a tool for developers to create, release and manage production ready containerized applications on ECS. From getting started, pushing to staging and releasing to production, the ECS CLI can help manage the entire lifecycle of your application development.

This is a small sample app that can be used to demonstrate the ECS CLI V2. It creates a static website using nginx as the frontend. 
## License

This library is licensed under the MIT-0 License. See the LICENSE file.


## ECS Circuit Breaker Example
```
Environment test is already on the latest version v1.7.0, skip upgrade.
✔ Proposing infrastructure changes for stack demo-test-api 
- Creating the infrastructure for stack demo-test-api                                [rollback complete]  [855.9s]
  The following resource(s) failed to create: [Service]. Rollback reques                                  
  ted by user.                                                                                            
  - Service discovery for your services to communicate within the VPC                [delete complete]    [0.0s]
  - Update your environment's shared resources                                       [update complete]    [114.5s]
    - A security group for your load balancer allowing HTTP and HTTPS traffic        [create complete]    [5.0s]
    - An Application Load Balancer to distribute public traffic to your services     [create complete]    [92.6s]
  - An IAM Role for the Fargate agent to make AWS API calls on your behalf           [delete complete]    [0.0s]
  - A CloudWatch log group to hold your service logs                                 [delete complete]    [4.0s]
  - An ECS service to run and maintain your tasks in the environment cluster         [delete complete]    [67.1s]
    Resource handler returned message: "Error occurred during operation 'E                                
    CS Deployment Circuit Breaker was triggered'." (RequestToken: 295a4734                                
    -71a8-4327-d588-a5751ce88c95, HandlerErrorCode: GeneralServiceExceptio                                
    n)                                                                                                    
    Deployments                                                                                            
               Revision  Rollout   Desired  Running  Failed  Pending                                               
      PRIMARY  2         [failed]  1        0        10      1                                                     
                                                                                                                   
    ✘ Latest failure event                                                                        
      - (service demo-test-api-Service-ZMAe8F2ERZtu) (deployment ecs-svc/65643                                     
        00971027597161) deployment failed: tasks failed to start.                                                  
  - A target group to connect the load balancer to your service                      [delete complete]    [0.0s]
  - An ECS task definition to group your containers and run them on ECS              [delete complete]    [1.7s]
  - An IAM role to control permissions for the containers in your tasks              [delete complete]    [4.0s]
✘ deploy service: stack demo-test-api did not complete successfully and exited with status ROLLBACK_COMPLETE
```

DNS name of load balancer
http://demo-Publi-B2558YQHQEVK-1579261678.ca-central-1.elb.amazonaws.com
http://demo-publi-b2558yqhqevk-1579261678.ca-central-1.elb.amazonaws.com/items/5?q=somequery

## Run locally w/ hot reload
`uvicorn api.main:app --reload`
api root - 127.0.0.1:60127  -> http://127.0.0.1:8000/items/5?q=somequery
docs root - 127.0.0.1:60128  -> http://127.0.0.1:8000/docs

## Run locally w/ Docker
`docker build -t myimage .`
`docker run -d --name container -p 8080:80 myimage`
http://127.0.0.1:8080/items/5?q=somequery

## Run locally w/ Docker Compose
# Builds images before starting containers.
`start-dev.sh` or `docker-compose up -d --build`


## Deploy
`copilot deploy -e test -w api`
specifcy copilot workload (service) and copilot environment
https://aws.github.io/copilot-cli/docs/concepts/services/#deploying-a-service

## Development
`pip install -r requirements.txt` - after cloning
`pip freeze > requirements.txt`  - after pip installing new package
