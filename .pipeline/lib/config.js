'use strict';
const options= require('@bcgov/pipeline-cli').Util.parseArguments()
const changeId = options.pr //aka pull-request
const version = '1.0.0'
const name = 'rsbc-dh'
const url_suffix = '.ocp.bitbox.ca'

const phases = {
  build: {namespace:'iowaey-tools',
    name: `${name}`,
    phase: 'build',
    transient: true, // auto clean build
    changeId:changeId,
    suffix: `-build-${changeId}`,
    instance: `${name}-build-${changeId}`,
    version:`${version}-${changeId}`,
    tag:`build-${version}-${changeId}`,
    url_suffix: `${url_suffix}`
  },
  dev: {namespace:'iowaey-dev',
    name: `${name}`,
    phase: 'dev',
    transient: true, // auto clean build
    changeId:changeId,
    suffix: `-dev-${changeId}`,
    instance: `${name}-dev-${changeId}`,
    version:`${version}-${changeId}`,
    tag:`dev-${version}-${changeId}`,
    url_suffix: `${url_suffix}`,
    cpu_request: '100m',
    cpu_limit: '200m',
    memory_request: '256Mi',
    memory_limit: '512Mi'
  },
  test: {namespace:'iowaey-test',
    name: `${name}`, phase: 'test',
    changeId:changeId, suffix: `-test`,
    instance: `${name}-test`,
    version:`${version}`,
    tag:`test-${version}`,
    url_suffix: `${url_suffix}`,
    cpu_request: '100m',
    cpu_limit: '200m',
    memory_request: '256Mi',
    memory_limit: '512Mi'
  },
  prod: {namespace:'iowaey-prod',
    name: `${name}`,
    phase: 'prod',
    changeId:changeId,
    suffix: `-prod`,
    instance: `${name}-prod`,
    version:`${version}`,
    tag:`prod-${version}`,
    url_suffix: `${url_suffix}`,
    cpu_request: '100m',
    cpu_limit: '200m',
    memory_request: '256Mi',
    memory_limit: '512Mi'
  }
};

// This callback forces the node process to exit as failure.
process.on('unhandledRejection', (reason) => {
  console.log(reason);
  process.exit(1);
});

module.exports = exports = {phases, options};
