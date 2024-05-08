FROM python:3.10

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8998
ENTRYPOINT ["python", "-m", "jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--port=8998", "--NotebookApp.token=''", "--NotebookApp.password=''"]
