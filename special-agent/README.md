# SpecialAgent Init Agent
A simple Dockerfile describing an image that can be used for bootstrapping pods in Kubernetes, by loading in the required dependencies for SpecialAgent instrumentation.
The SpecialAgent jar files are compiled using our [fork](https://github.com/xitric/java-specialagent) of the SpecialAgent project.
