# SockShop Deployments
This directory contains deployment configurations for the modified SockShop application on Amazon Elastic Container Service (ECS) and in Docker-compose. These deployments have been used to evaluate the feasibility of using OpenTelemetry to collect telemetry data from applications in these environments. This directory also contains deployment files for a simple Fluentd service that sends logs to Humio.

We do not claim ownership of the deployment inside `docker-compose`. Furthermore, the deployment to Amazon ECS is based on the official deployment script for SockShop, but we have been required to make extensive changes to remove the proprietary Weave Scope service discovery tool. This necessitated a number of changes:

- Change all networking configurations, including EC2 host network modes, VPC, and NAT Gateways.
- Perform service discovery using the Amazon Route 53 DNS.
- Add our custom-built OpenTelemetry collector with the Humio exporter to collect traces and send them to Humio.
- Completely rework the ECS launch configuration.
- Completely rework all role policies.

For this reason, not much is left from the original deployment script, except for some initialization procedures of databases.
