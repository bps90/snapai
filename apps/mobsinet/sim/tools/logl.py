import logging

# Constants for logging levels
ALWAYS = True
EVENT_QUEUE_DETAILS = False
ERROR_DETAIL = True
WARNING = True
INFO = True
HINTS = True
ROUND_DETAIL = False
MESSAGE_DETAIL = False
INTERFERENCE_DETAIL = False
NODE_DETAIL = False
CONNECTIVITY_DETAIL = False
GUI_SEQ = False
GUI_DETAIL = False
GUI_ULTRA_DETAIL = False


class LogL:
    def __init__(self, log_file, log_level=logging.DEBUG):
        self.log_file = log_file
        
        # Create a logger instance
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)  # Set the logging level
        
        # Create a file handler for logging to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)  # Set the file handler's logging level
        
        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Add formatter to file handler
        file_handler.setFormatter(formatter)
        
        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
    
    def log_always(self, message):
        if ALWAYS:
            self.logger.info(message)
    
    def log_event_queue_details(self, message):
        if EVENT_QUEUE_DETAILS:
            self.logger.debug(message)
    
    def log_error_detail(self, message):
        if ERROR_DETAIL:
            self.logger.error(message)
    
    def log_warning(self, message):
        if WARNING:
            self.logger.warning(message)
    
    def log_info(self, message):
        if INFO:
            self.logger.info(message)
    
    def log_hints(self, message):
        if HINTS:
            self.logger.info(message)
    
    def log_round_detail(self, message):
        if ROUND_DETAIL:
            self.logger.debug(message)
    
    def log_message_detail(self, message):
        if MESSAGE_DETAIL:
            self.logger.debug(message)
    
    def log_interference_detail(self, message):
        if INTERFERENCE_DETAIL:
            self.logger.debug(message)
    
    def log_node_detail(self, message):
        if NODE_DETAIL:
            self.logger.debug(message)
    
    def log_connectivity_detail(self, message):
        if CONNECTIVITY_DETAIL:
            self.logger.debug(message)
    
    def log_gui_seq(self, message):
        if GUI_SEQ:
            self.logger.debug(message)
    
    def log_gui_detail(self, message):
        if GUI_DETAIL:
            self.logger.debug(message)
    
    def log_gui_ultra_detail(self, message):
        if GUI_ULTRA_DETAIL:
            self.logger.debug(message)

# Example usage:
if __name__ == "__main__":
    logger = LogL("app.log", logging.INFO)  # Optional: specify logging level
    
    logger.log_always("This is an 'ALWAYS' level message.")
    logger.log_event_queue_details("This is an 'EVENT_QUEUE_DETAILS' level message.")
    logger.log_error_detail("This is an 'ERROR_DETAIL' level message.")
    logger.log_warning("This is a 'WARNING' message.")
    logger.log_info("This is an 'INFO' message.")
    logger.log_hints("This is a 'HINTS' message.")
    logger.log_round_detail("This is a 'ROUND_DETAIL' level message.")
    logger.log_message_detail("This is a 'MESSAGE_DETAIL' level message.")
    logger.log_interference_detail("This is an 'INTERFERENCE_DETAIL' level message.")
    logger.log_node_detail("This is a 'NODE_DETAIL' level message.")
    logger.log_connectivity_detail("This is a 'CONNECTIVITY_DETAIL' level message.")
    logger.log_gui_seq("This is a 'GUI_SEQ' level message.")
    logger.log_gui_detail("This is a 'GUI_DETAIL' level message.")
    logger.log_gui_ultra_detail("This is a 'GUI_ULTRA_DETAIL' level message.")
