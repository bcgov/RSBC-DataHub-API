# JH-ETK Network Policies

This readme summarizes the network policies required for the RSBC Digital Forms (RSBC-DF) to operate in OpenShift 4.x namespaces.

## Policies

### deny-by-default

    The default posture for a security first namespace is to
    deny all traffic. If not added this rule will be added
    by Platform Services during environment cut-over.

### allow-from-openshift-ingress

    This policy allows any pod with a route & service combination
    to accept traffic from the OpenShift router pods. This is
    required for things outside of OpenShift (like the Internet)
    to reach your pods.

### allow-all-internal

    Allow all pods within the current namespace to communicate
    to one another.

## Applying rsbc-df network policies

`` oc process -f rsbc-df-policies.yaml -p NAMESPACE_PREFIX=<LICENCE_PLATE_HERE> -p ENVIRONMENT=<ENVIRONMENT_NAME_HERE> | oc -n <LICENCE_PLATE_HERE>-<ENVIRONMENT_NAME_HERE> apply -f - ``

e.g., applying the network policies in the be78d6-dev namespace (RSBC Digital Forms Dev Environment):

`` oc process -f rsbc-df-policies.yaml -p NAMESPACE_PREFIX=be78d6 -p ENVIRONMENT=dev | oc -n be78d6-dev apply -f - ``
