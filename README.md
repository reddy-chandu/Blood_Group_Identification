<div align="center">

# Blood Group Identification using Python

### An image-processing prototype for ABO and Rh blood-group classification

A Django web application that accepts an ABD blood-sample image, processes it with OpenCV, and displays a rule-based blood-group estimate.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-Web%20app-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Image%20processing-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)

</div>

## 💡 About The Project

This project combines image processing with a web-based user workflow to demonstrate blood-group classification from ABD blood-sample images. Users can create an account, sign in, upload an image, and view the original image, its processed version, and the resulting ABO/Rh estimate. Account flows use Django's built-in authentication and CSRF middleware; the interface uses Bootstrap.

The classification logic is an image-processing heuristic, not a trained machine-learning model. It divides the processed image into A, B, and D regions and uses connected-component counts to infer the ABO group and Rh factor.

### How It Works

1. An authenticated user uploads an ABD blood-sample image.
2. OpenCV converts the image to grayscale, applies Gaussian blur and histogram equalization, then uses Otsu thresholding and morphological opening/closing.
3. The processed image is divided into A, B, and D regions. Connected components are counted in each region.
4. A and B counts determine the estimated ABO group; a detected component in the D region determines the estimated Rh factor.
5. The application displays the uploaded image, processed image, and estimated result.

### Built With

* **Frontend:** HTML, CSS, Bootstrap
* **Backend:** Python, Django
* **Image processing:** OpenCV, NumPy
* **Database:** PostgreSQL

## 🚀 Getting Started

Follow these instructions to run the project locally.

### Prerequisites

* Python 3.13
* `pip`
* Access to a PostgreSQL database (e.g., Supabase, Neon, Railway, AWS RDS) with the corresponding DATABASE_URL configured.

### Installation

1. **Clone the repository**
   ```powershell
   git clone https://github.com/reddy-chandu/Blood_Group_Identification.git
   cd Blood_Group_Identification
   ```

2. **Create and activate a virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   *(For macOS/Linux, use: `source .venv/bin/activate`)*

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   The Django settings load variables from a `.env` file in the repository root. Set a Django secret key and a database URL for a reachable database:

   ```dotenv
   SECRET_KEY=replace-with-a-private-django-secret-key
   DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DB_NAME
   ```

   Keep real credentials private; do not commit them. The configured database URL requires SSL. Use an appropriate SSL-enabled database connection for your environment.

5. **Apply database migrations**
   ```powershell
   python manage.py migrate
   ```

6. **Start the development server**
   ```powershell
   python manage.py runserver
   ```

7. **Access the web app**

   Open your browser and navigate to

   ```
   http://127.0.0.1:8000
   ```

## 📁 Project Architecture

```text
Blood_Group_Identification/
├── manage.py                         # Django management entry point
├── requirements.txt                  # Python dependencies
├── Blood_Group_Identification/
│   ├── settings.py                   # Django and database configuration
│   ├── urls.py                       # Application routes
│   ├── asgi.py
│   └── wsgi.py
└── users/
    ├── views.py                      # Authentication and OpenCV classification
    ├── templates/
    │   ├── home.html                 # Landing page
    │   ├── login.html                # Sign-in page
    │   ├── signup.html               # Registration page
    │   └── profile.html              # Image upload and result page
    └── static/                       # Images used by the web interface
```

## ⚠️ Important Disclaimers

> **Medical disclaimer:** This project is an educational prototype, not a medical device or a validated diagnostic method. Its image-processing heuristic must not be used to determine a person's blood type or guide medical decisions. Blood typing must be performed by a qualified laboratory using validated procedures.

## 📝 License

Distributed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.
 