#!/usr/bin/env bash
declare DIR=$(realpath ${BASH_SOURCE%/*})
declare customdir=''

declare projname='TextWrapperDev'

if [[ "$1" =~ ^d ]]; then
  if [[ "$customdir" ]]; then
    rm "${customdir}/${projname}"

  elif [[ $(uname) = 'Darwin' ]]; then
    rm ~"/Library/Application\ Support/Anki2/addons21/${projname}"

  elif [[ $(uname) = 'Linux' ]]; then
    rm ~"/.local/share/Anki2/addons21/${projname}"

  else
    echo 'Unknown platform'
    exit -1
  fi

else
  if [[ $customdir ]]; then
    ln -s "${DIR}" "${customdir}/${projname}"

  elif [[ $(uname) = 'Darwin' ]]; then
    ln -s "${DIR}" ~"/Library/Application Support/Anki2/addons21/${projname}"

  elif [[ $(uname) = 'Linux' ]]; then
    ln -s "${DIR}" ~"/.local/share/Anki2/addons21/${projname}"

  else
    echo 'Unknown platform'
    exit -1
  fi
fi
