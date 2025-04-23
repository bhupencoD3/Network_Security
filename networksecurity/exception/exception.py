"""
Custom exception class for the NetworkSecurity package.

Includes details like the exact line number and file name where the exception occurred.
"""

import sys


class NetworkSecurityException(Exception):
    """Base class for all exceptions in the NetworkSecurity package."""

    def __init__(self, error_message, error_details: sys):
        """
        Initialize with an error message and system error details.

        Parameters:
        - error_message (str): The error message to display.
        - error_details (sys): Typically passed as `sys` to extract traceback info.
        """
        super().__init__(error_message)
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occurred in script: [{self.file_name}] "
            f"at line number: [{self.line_number}] "
            f"with error message: [{self.error_message}]"
        )
