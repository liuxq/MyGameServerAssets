#!/bin/sh

export KBE_ROOT=$(cd ../; pwd)
export KBE_RES_PATH="$KBE_ROOT/kbe/res/:$KBE_ROOT/MyGameServerAssets:$KBE_ROOT/MyGameServerAssets/res/:$KBE_ROOT/MyGameServerAssets/scripts/"
export KBE_BIN_PATH="$KBE_ROOT/kbe/bin/server/"

echo KBE_ROOT = \"${KBE_ROOT}\"
echo KBE_RES_PATH = \"${KBE_RES_PATH}\"
echo KBE_BIN_PATH = \"${KBE_BIN_PATH}\"

$KBE_BIN_PATH/bots&

