import unittest
import threading
import time
import os
from unittest import mock
import tempfile
import subprocess
import shutil

from sqlflow.client import Client
from tests.mock_servicer import _server, MockServicer

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any
import sqlflow.server.proto.sqlflow_pb2 as pb

def generateTempCA():
    tmp_dir = tempfile.mkdtemp(suffix="sqlflow_ssl", dir="/tmp")
    ca_key = os.path.join(tmp_dir, "ca.key")
    ca_csr = os.path.join(tmp_dir, "ca.csr")
    ca_crt = os.path.join(tmp_dir, "ca.crt")

    assert subprocess.call(["openssl", "genrsa", "-out", ca_key, "2048"]) == 0
    assert subprocess.call(["openssl", "req", "-nodes", "-new", "-key", ca_key, "-subj", "/CN=localhost", "-out", ca_csr]) == 0
    assert subprocess.call(["openssl", "x509", "-req", "-sha256", "-days", "365", "-in", ca_csr, "-signkey", ca_key, "-out", ca_crt]) == 0

    return tmp_dir, ca_crt, ca_key


class ClientServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # TODO: free port is better
        port = 8765
        cls.event = threading.Event()
        cls.tmp_ca_dir, ca_crt, ca_key = generateTempCA()
        threading.Thread(target=_server, args=[port, cls.event, ca_crt, ca_key]).start()
        # wait for start
        time.sleep(1)
        cls.client = Client("localhost:%d" % port, ca_crt)

    @classmethod
    def tearDownClass(cls):
        # shutdown server after this test
        cls.event.set()
        shutil.rmtree(cls.tmp_ca_dir, ignore_errors=True)

    def test_execute_stream(self):
        with mock.patch('sqlflow.client._LOGGER') as log_mock:
            self.client.execute("select * from galaxy train ..")
            log_mock.info.assert_called_with("extended sql")

        expected_table = MockServicer.get_test_table()
        rows = self.client.execute("select * from galaxy")
        assert expected_table["column_names"] == rows.column_names()
        assert expected_table["rows"] == [r for r in rows.rows()]

    def test_decode_time(self):
        any_message = Any()
        timestamp_message = Timestamp()
        timestamp_message.GetCurrentTime()
        any_message.Pack(timestamp_message)
        assert timestamp_message.ToDatetime() == Client._decode_any(any_message)

    def test_decode_null(self):
        any_message = Any()
        null_message = pb.Row.Null()
        any_message.Pack(null_message)
        assert Client._decode_any(any_message) is None
