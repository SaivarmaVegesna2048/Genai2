import logging
import os
from datetime import datetime

logs=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)
log_file=os.path.join(log_path,logs)
logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    format="[%(asctime)s]-%(lineno)d-%(name)s-%(levelname)s-%(message)s")