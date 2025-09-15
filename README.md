# RelaFit - Installation Guide

Greetings! 😊

Follow these steps to run **NextDoorDeals** smoothly on **Windows**.

---

## 📋 Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.13.1**  
  Download from the official site:  
  [https://www.python.org/downloads/release/python-3131/](https://www.python.org/downloads/release/python-3131/)

## 🚀 Installation Steps

### 1. Download the Project

- Go to the [RelaFit GitHub repository](https://github.com/MariaAcevedo11/RelaFit).
- Click the green **"Code"** button and select **"Download ZIP"**.
- Extract the contents.

---

### 2. Set Up the Project Directory

- *(Optional but recommended)* Create a folder named `rela` on your desktop and move the extracted `RelaFit` folder inside it.
- Navigate to the `RelaFit` folder.
- Copy its full path:

  Click the address bar in File Explorer and press `CTRL + C`.


### 3. Open the Command Line

Open a terminal and navigate to the project folder:

```bash
cd <PASTED_PATH>
```

Example (Windows):

```bash
cd C:\Users\maria\Desktop\rela\RelaFit
```

---
### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Server

```bash
python manage.py runserver
```
### 6. Open the Web Application

Open your browser and go to:

```
http://localhost:8000/
```

You should now see the **RelaFit** homepage. 🎉

---
