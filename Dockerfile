FROM python:3.8

COPY requirements.txt ./requirements.txt

RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["streamlit.py"]