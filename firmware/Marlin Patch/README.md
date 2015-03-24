Patch for Marlin
------------------------

Adds support for waiting for queued movements before toggling GPIOs

To apply patch first clone the Marlin repository:
    $ git clone git@github.com:MarlinFirmware/Marlin.git

Then run the patch command inside the repository:
    $ git am <patch_file>

Note: this patch was applied to commit 512a005. If patching to latest commit fails,
try to patch that one
