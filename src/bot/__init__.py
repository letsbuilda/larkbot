import logging

# Some basic logging to get existing loggers to show
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("discord").setLevel(logging.INFO)
