import subprocess
import time

import pytest

from common.constants.tests import HealthChecksConstants
from healthchecks.api_server.test_data import valid_stdout_data
from utils.tests import find_fullpath


class TestCaseDevStartup:

    @pytest.mark.skip(reason='need more time to figure out this healthceck.')
    @pytest.mark.asyncio
    async def test_dev_run_py_valid_stdout_messages(self) -> None:
        """Test development run.py file for valid uvicorn and fastapi startup stdout messages.

        Returns:
        Nothing.
        """
        run_filepath = find_fullpath(
            HealthChecksConstants.API_SERVER_STARTUP_FILENAME.value,
            HealthChecksConstants.ROOT_FILEPATH.value,
        )
        api_server_run_process = subprocess.Popen(
            ['python', run_filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        time.sleep(HealthChecksConstants.STDOUT_TIMEOUT_SEC.value)
        api_server_run_process.terminate()
        outputs = [line.decode('utf-8').strip() for line in api_server_run_process.stdout.readlines()]
        print(outputs)
        assert valid_stdout_data.VALID_UVICORN_STDOUT_MSG in outputs
        assert valid_stdout_data.VALID_FASTAPI_STARTUP_STDOUT_MSG in outputs
