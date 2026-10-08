import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL","sqlite:///./certificate_generator.db")
GENERATED_DIR=Path(os.getenv("GENERATED_DIR","generated"))
MAX_RECIPIENTS=int(os.getenv("MAX_RECIPIENTS","1000"))
GENERATED_DIR.mkdir(parents=True,exist_ok=True)
