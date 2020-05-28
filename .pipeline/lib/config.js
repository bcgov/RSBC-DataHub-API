'use strict';
const options= require('@bcgov/pipeline-cli').Util.parseArguments()
const changeId = options.pr //aka pull-request
const name = 'rsbc-dh'
const url_suffix = '.pathfinder.gov.bc.ca'

const phases = {
  build: {namespace:'iowaey-tools',
    name: `${name}`,
    phase: 'build',
    transient: 'true', // auto clean build
    changeId:changeId,
    suffix: `-build-${changeId}`,
    instance: `${name}-build-${changeId}`,
    version:`build-${changeId}`,
    tag:`build-${changeId}`,
    url_suffix: `${url_suffix}`
  },
  pr: {namespace:'iowaey-dev',
    name: `${name}`,
    phase: 'pr',
    transient: 'true', // auto clean build
    changeId:changeId,
    suffix: `-pr-${changeId}`,
    instance: `${name}-pr-${changeId}`,
    version:`pr`,
    tag:`pr-${changeId}`,
    url_suffix: `${url_suffix}`,
    db_host: 'clockwork.idir.bcgov',
    db_name: 'rsbcodw',
    cpu_request: '100m',
    cpu_limit: '200m',
    memory_request: '256Mi',
    memory_limit: '512Mi'
  },
  dev: {namespace:'iowaey-dev',
    name: `${name}`,
    phase: 'dev',
    transient: 'true', // auto clean build
    changeId:changeId,
    suffix: `-dev`,
    instance: `${name}-dev-${changeId}`,
    version:`dev`,
    tag:`dev-${changeId}`,
    url_suffix: `${url_suffix}`,
    db_host: 'clockwork.idir.bcgov',
    db_name: 'rsbcodw',
    cpu_request: '100m',
    cpu_limit: '200m',
    memory_request: '256Mi',
    memory_limit: '512Mi'
  },
  test: {namespace:'iowaey-test',
    name: `${name}`, phase: 'test',
    changeId:changeId, suffix: `-test`,
    suffix: `-test`,
    instance: `${name}-test`,
    version:`test`,
    tag:`test`,
    url_suffix: `${url_suffix}`,
    db_host: 'clockwork.idir.bcgov',
    db_name: 'rsbcodw',
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
    version:`prod`,
    tag:`prod`,
    url_suffix: `${url_suffix}`,
    db_host: 'burden.idir.bcgov',
    db_name: 'rsbcodw',
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
