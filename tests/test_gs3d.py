import unittest
from unittest.mock import patch, MagicMock
import sys
import argparse

# Add src directory to sys.path to allow importing GS3D
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from GS3D import S3Downloader, main as gs3d_main 

class TestS3DownloaderArgs(unittest.TestCase):
    @patch('GS3D.S3Downloader') # Mock the S3Downloader class
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_passes_endpoint_url(self, mock_parse_args, MockS3Downloader):
        # Simulate providing the endpoint_url argument
        mock_args = argparse.Namespace(
            s3_url='s3://bucket/key',
            profile=None,
            access_key=None,
            secret_key=None,
            region=None,
            output_dir=None,
            max_workers=5,
            anonymous=False,
            keep_structure=False,
            endpoint_url='http://localhost:9000' # Test value
        )
        mock_parse_args.return_value = mock_args
        
        # Mock the download method to prevent actual download
        mock_downloader_instance = MockS3Downloader.return_value
        mock_downloader_instance.download.return_value = True

        with patch.object(sys, 'exit') as mock_exit: # Patch sys.exit
             gs3d_main()


        # Check if S3Downloader was instantiated with the endpoint_url
        MockS3Downloader.assert_called_once_with(
            s3_url='s3://bucket/key',
            profile_name=None,
            access_key=None,
            secret_key=None,
            region=None,
            output_dir=None,
            max_workers=5,
            anonymous=False,
            endpoint_url='http://localhost:9000' # Ensure this is passed
        )

class TestS3ClientInitialization(unittest.TestCase):
    @patch('boto3.client') # Mock boto3.client directly
    def test_initialize_s3_client_with_endpoint(self, mock_boto3_client):
        downloader = S3Downloader(s3_url='s3://test-bucket/test-key', endpoint_url='http://custom.endpoint:1234', anonymous=False) # Explicitly set anonymous to False for clarity
        downloader = S3Downloader(s3_url='s3://test-bucket/test-key', endpoint_url='http://custom.endpoint:1234', anonymous=False) # Explicitly set anonymous to False for clarity
        
        # Mock head_object to prevent actual S3 calls during _check_key_type
        mock_s3_instance = MagicMock()
        # mock_s3_instance.head_object.side_effect = Exception("Simulated S3 error for head_object") # Keep this commented unless specific test for it
        mock_boto3_client.return_value = mock_s3_instance
        
        # We need to parse the URL first to set bucket_name and key
        downloader._parse_s3_url(downloader.s3_url)
        
        # Call the method that initializes the client
        downloader._initialize_s3_client()

        # Assert that boto3.client was called with the endpoint_url
        # Config should not be present if anonymous is False and no default creds are assumed to trigger the fallback
        mock_boto3_client.assert_called_with(
            's3',
            endpoint_url='http://custom.endpoint:1234'
            # No config here if not anonymous
        )

    @patch('boto3.Session') # Mock boto3.Session for profile/key based auth
    def test_initialize_s3_client_with_endpoint_and_keys(self, MockBotoSession):
        mock_session_instance = MockBotoSession.return_value
        # mock_s3_client_instance = mock_session_instance.client.return_value # Not used in assertion for this test

        downloader = S3Downloader(
            s3_url='s3://test-bucket/test-key',
            access_key='test_ak',
            secret_key='test_sk',
            endpoint_url='http://custom.endpoint:5678'
        )
        downloader._parse_s3_url(downloader.s3_url)
        downloader._initialize_s3_client()

        mock_session_instance.client.assert_called_with(
            's3',
            endpoint_url='http://custom.endpoint:5678'
        )

if __name__ == '__main__':
    unittest.main()
