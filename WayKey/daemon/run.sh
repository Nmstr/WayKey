DIR="$( cd "$( dirname "$( readlink -f "${BASH_SOURCE[0]}" )" )" &> /dev/null && pwd )"
cd "${DIR}/../../" || exit 1
. "${DIR}/../../.venv/bin/activate"
python3 "${DIR}/main.py" "$@"
