# Proyek Analisis Data E-Commerce

## Setup Environment

### Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Setup Environment - Shell/Terminal (pipenv)

```bash
mkdir E-Commerce-Data-Analysis-Project
cd E-Commerce-Data-Analysis-Project
pipenv install
pipenv shell
pip install -r requirements.txt
```

### Setup Environment - Virtual Environment (venv)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

---

## Run Streamlit App

```bash
streamlit run dashboard.py
```
