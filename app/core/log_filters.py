import logging

class HealthCheckFilter(logging.Filter):
    """Filter out health check requests from logs"""
    
    def __init__(self, path="/health"):
        super().__init__()
        self.path = path
    
    def filter(self, record):
        # Check if the record has a message attribute and contains the health check path
        if hasattr(record, 'message'):
            return self.path not in record.message
        # For records that haven't been formatted yet, check the raw message
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            return self.path not in record.msg
        return True
