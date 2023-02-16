# Contributing to this project

## Forks

The repository doesn't accept direct changes and does not support in-repo branches. To contribute, fork the repository, make your changes in the forked repository, and submit a PR for the team's review.

## Developer setup

TBD

## Build and test

Every deployable container has its own dockerfile which includes the entire CI pipeline - build, verify quality and run all tests. The philosophy behind this is to ensure that if a container can be created only when all its tests are passed, and it makes the CI/CD process repeatable everywhere, independently from the environment that invokes it.

A component individual CI pipeline will be triggered for every pull request opened in the main repository. 
The CD pipeline will be triggered when a PR is merged. A PR cannot be merged unless it was reviewed and approved by a team member, and passed the image build which includes 100% passing unit tests.

Once the CD pipeline is successful, the image will be tagged as 'latest' and pushed to Artifactory for deployment into the development environment.

## Coding standards

TBD

## Versioning

Each CD execution will tag the repository with `<image name>=v<version>` lightweight tag. The version for each component follow semver and uses [Angular commit message conventions](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines) to handle major, minor and patch versions.

The version will be set as an environment variable in the generated container image, and the image will also be tagged with the version when pushed to the image registry (BC Gov Artifactory service).