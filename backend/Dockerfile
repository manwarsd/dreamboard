FROM python:3.12-slim

# so logs show up immediately
ENV PYTHONUNBUFFERED=1

# 1) set working dir
WORKDIR /code

# 2) install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 3) copy your entrypoint
COPY main.py .

# 4) copy your app package
COPY app/ app/

# 5) ensure Python can import from app/
ENV PYTHONPATH="${PYTHONPATH}:/code/app"

# 6) launch via uvicorn
#    - if your ROOT main.py defines `app = FastAPI()` use "main:app"
#    - if instead you want to run app/main.py, use "app.main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
