"use strict";
const { OpenShiftClientX } = require("@bcgov/pipeline-cli");
const path = require("path");

module.exports = settings => {
  const phases = settings.phases;
  const options = settings.options;
  const oc = new OpenShiftClientX(Object.assign({ namespace: phases.build.namespace }, options));
  const phase = "build";
  let objects = [];
  const templatesLocalBaseUrl = oc.toFileUrl(path.resolve(__dirname, "../../openshift"));

  // The building of your cool app goes here ▼▼▼
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-ingestor-build.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'SOURCE_REPOSITORY_URL': oc.git.http_url,
      'SOURCE_REPOSITORY_REF': oc.git.ref,
      'SOURCE_CONTEXT_DIR': 'ingestor'
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-validator-build.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'SOURCE_REPOSITORY_URL': oc.git.http_url,
      'SOURCE_REPOSITORY_REF': oc.git.ref,
      'SOURCE_CONTEXT_DIR': 'validator'
    }
  }))
  objects.push(...oc.processDeploymentTemplate(`${templatesLocalBaseUrl}/rsbcdh-writer-build.yaml`, {
    'param':{
      'NAME': phases[phase].name,
      'SUFFIX': phases[phase].suffix,
      'VERSION': phases[phase].tag,
      'SOURCE_REPOSITORY_URL': oc.git.http_url,
      'SOURCE_REPOSITORY_REF': oc.git.ref,
      'SOURCE_CONTEXT_DIR': 'writer'
    }
  }))

  oc.applyRecommendedLabels(
    objects,
    phases[phase].name,
    phase,
    phases[phase].changeId,
    phases[phase].instance,
  );
  oc.applyAndBuild(objects);
};
