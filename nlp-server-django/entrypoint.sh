#!/bin/bash
# entrypoint.sh

# Run the post-install script
bash ./scripts/post_install.sh

# Proceed to CMD
exec "$@"