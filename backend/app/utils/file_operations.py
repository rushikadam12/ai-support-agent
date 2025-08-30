import os,shutil
from utils.logger import log_info
from datetime import datetime

def save_file(file,session_id)->str|None:
    try:
        file_name=f"{session_id}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.pdf"
        base_path=os.getcwd()
        dir_name="session"
        file_path=os.path.join(base_path,dir_name,file_name)

        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(file.file,buffer)

        return file_path
    except Exception as error:
        log_info("save_file-------->",str(error))
        return None
