#!/bin/bash
# The common tree carries recovery-only modules that have no counterpart in a
# full source tree, so let the build proceed past them.
export ALLOW_MISSING_DEPENDENCIES=true
