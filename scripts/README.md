Use the scripts in this directory
to create Openshift secrets.  

- copy and rename the *.secrets.example.sh to 
*.secrets.sh
- create one secret file for each environment:
  - rsbc-dh-dev-secrets.sh
  - rsbc-dh-test-secrets.sh
  - rsbc-dh-prod-secrets.sh
- edit each script to include hard coded secrets
- all files ending in *.secrets.sh files are ignored by Git
