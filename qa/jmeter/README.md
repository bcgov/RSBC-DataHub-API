# JMeter script to test core DFDH workflow

JMeter and the wrapper script in this folder were used with [Apache JMeter](https://jmeter.apache.org/) to verify the DFDH 1.0 release workflow in late 2020 and early 2021. This approach no longer works because the DFAPI is now only accessible from within the DEV or TEST namespaces (the DFAPI request must originate from inside a pod in the namespace, so you cannot even forward a local port to a pod). This is more secure, but is less convenient for testing.

The JMeter script and its wrapper are committed here as a reference. There's a video of it running on the [DFAPI 1.0.0 production release page](https://justice.gov.bc.ca/wiki/display/RDFP/DFAPI+1.0.0%3A+2020-10-07+production+release). See the [DF wiki JMeter page](https://justice.gov.bc.ca/wiki/display/RDFP/DFAPI%3A+JMeter+test+suite) for variations. Note: URIs and credentials are parameterised and must be loaded from an environment script. See template.env for an example. Use template.env as a starting point if you want to create a JMeter project in the future.

JMeter is a great tool, and is well suited to doing functional testing on an API if you don't mind the old Java interface.

Call JMeter from the wrapper script run-jmeter.sh, which will load in the appropriate local environment file. 


## JMeter installation

The JMeter included in the Ubuntu repos is obsolete. Install it directly by downloading the binary from https://jmeter.apache.org/download_jmeter.cgi and putting it somewhere like ~/bin. Add the JMeter bin folder to the PATH environment variable.