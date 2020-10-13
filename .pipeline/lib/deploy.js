"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");
const path = require("path");

module.exports = settings => {
  const phases = settings.phases;
  const options = settings.options;
  const phase = options.env;
  const changeId = phases[phase].changeId;
  const oc = new OpenShiftClientX(Object.assign({ namespace: phases[phase].namespace }, options));

  const templatesLocalBaseUrl = oc.toFileUrl(path.resolve(__dirname, "../../openshift"));
  var objects = [];

  // The deployment of your cool app goes here ▼▼▼
  console.log('Delete routes...')
  oc.raw('delete', ['route'], {selector:`app=${phases[phase].instance},env-name=${phases[phase].phase},github-repo=${oc.git.repository},github-owner=${oc.git.owner}`, wait:'true', namespace:phases[phase].namespace})

  //First call will create/generate default secret values frome a pre-existing manually created template secret object
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-secrets.yaml`, {
   'param':{
     'NAME': `${phases[phase].name}-${phases[phase].phase}`,
     'SUFFIX': phases[phase].suffix
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-rabbitmq-deploy.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-paybc-deploy.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-form-handler-deploy.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-hold-processor-deploy.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-geocoder-deploy.yaml`, {
    'param': {
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-ingestor-deploy.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-validator-deploy.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-writer-deploy.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'PHASE': phases[phase].phase,
      'URL_SUFFIX': phases[phase].url_suffix,
      'DB_HOST': phases[phase].db_host,
      'DB_NAME': phases[phase].db_name,
      'CPU_REQUEST': phases[phase].cpu_request,
      'CPU_LIMIT': phases[phase].cpu_limit,
      'MEMORY_REQUEST': phases[phase].memory_request,
      'MEMORY_LIMIT': phases[phase].memory_limit
    }
  }))

  oc.applyRecommendedLabels(
    objects,
    phases[phase].name,
    phase,
    `${changeId}`,
    phases[phase].instance,
  );
  oc.importImageStreams(objects, phases[phase].tag, phases.build.namespace, phases.build.tag);
  oc.applyAndDeploy(objects, phases[phase].instance);
};
