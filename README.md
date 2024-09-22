# django

## Setup 


### Environment Setup

```

    ## Windows
        $ cd onedrive\desktop\code
        $ mkdir drf
        $ cd drf
        $ python -m venv .venv
        $ .venv\Scripts\Activate.ps1
        (.venv) $ 
```

```
    ## macOS
        $ cd desktop/desktop/code
        $ mkdir drf
        $ cd drf
        $ python3 -m venv .venv
        $ source .venv/bin/activate
        (.venv) $
``` 

if want to do through visual studio 

```

    # macOS
        $ cd desktop/desktop/code
        $ mkdir drf
        $ cd drf
        $ code .
        $ python3 -m venv .venv
        $ source .venv/bin/activate
        (.venv) $ 
```

Sometimes you may not see it, but to double check in VS Code you can do command + Shift + p --> then check for python interpreter

### Required Installation 

Just like adding the required dependency

```
python -m pip install django
python -m pip install djangorestframework

pip install django-cors-headers 
```

Save the information about virtual environment in requirements.txt file 

```
pip freeze > requirements.txt
```

### Create Required Project now

Now with the installation, we can create the final project using `django-admin startproject <name of project> .`.

`.` will help us to create in same directory otherwise it will create a new directory for startproject. 

django-admin startproject <name of project> .
```
django-admin startproject djangoBasics . 
```

Moreover, we need to add component for this project. They are called using `startapp`. It represents, some component of the project. A project can have multiple `startapp` representing different features. 


python manage.py startapp <name of application>

```
python manage.py startapp ftpFileDownload
```

### Register the installations in Project

Go to `config` in `<nameOfProject>/settings.py` file. Add it to `INSTALLED_APPS`



```python
# djangoBasics/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Installations
    'rest_framework',
    'corsheaders',

    #Add the app here
    'ftpFileDownload',
    
]
```

Added step for CORS:
1. In `MIDDLEWARE` add `corsheaders.middleware.CorsMiddleware`

    ```python

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        #...
    ]
    ```
2. Specify which domains you want to give access to by doing the following in settings.py file

    ```
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        #...
    ]
    
    # Add configuration here
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = (
        'http://localhost:8000',
        ) 
    ```

### Initial Run for project

1. Now you can check by starting the server if everything is working fine. : 

    ```
        $   python manage.py runserver
    ```
2. Go to localhost and you will see the image: `http://127.0.0.1:8000/`
3. In terminal you can see the error :
   ```
    You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.
    September 22, 2024 - 09:16:31
    Django version 5.1.1, using settings 'djangoBasics.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
   ```
4. Migrations are important to sync models with database even if it's not present let's do this. Also if you add any Models (Entity), we need to run migraiton to keep the project in sync
   1. `python manage.py makemigrations <appName>`
   
    ```
        $ python manage.py makemigrations ftpFileDownload 
        $ python manage.py migrate
    ```
5. Run the server again 
    ```
        $   python manage.py runserver
    ```
6. You will not find any error
   ```
   Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    September 22, 2024 - 09:23:31
    Django version 5.1.1, using settings 'djangoBasics.settings'
    Starting development server at http://127.0.0.1:8000/
   ```

## Coding Starts here


### Create a Serializer (Java-DTO)

Serializers behave just like a DTO for a particular app.
- Location: `<appName>/serializers.py`

- Add a  `ftpFileDownload/serializers.py` to mimic a dto, which will receive information from the API, using request parameter. 

```python
from rest_framework import serializers

class ClientInfoSerializer(serializers.Serializer):
    # Validations are also added for the format
    date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    ticker = serializers.CharField(max_length=10)



```


### Modify the VIEW (Java - Controller/Service)

View helps us to define the API's.
- Location : `<appName>/views.py`

```

```
### Configure Application URLs using views.py

Now, we need to reach to this particular app (Act as RestController)

- Create or update file called : `<appName>/urls.py`

```python

from django.urls import path

# Import the API that has been created, and configure the URLs
from .views import GetClientInfoUsingTickerNameAndDate

urlpatterns = [
    path('get-client-data/', GetClientInfoUsingTickerNameAndDate.as_view(), name='get-client-data'),
]
```

### Modify the Base Project for URLs

- Go to `<ProjectName>/urls.py` to register the Application urls

```python
    from django.contrib import admin

    # include, will help to point to other urls configurations for different pages
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        #Configuring the API, stating that all the URLS starting from api/ftp will be redirected to ftpFileDownload.urls
        #Prefix: /api/ftp
        path('api/ftp/',include('ftpFileDownload.urls'))
    ]

```

## Frontend to get the formData

### Template for apps : index.html

- Create a **templates** folder in the `<appName>`, for which UI is being made
- Create the `index.html` file to add html codes
- `onclick="fetchData()"`: Once you click on the form, this function is called in **script**, which will inturn call the backend API
  
-   fetch(`/api/ftp/get-client-data?date=${date}&ticker=${ticker}`) : By default it's get, so it will just call the api with parameters
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FTP</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">

    <style>
        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #3f51b5;
        }
        .mdc-text-field {
            width: 100%;
            margin-bottom: 20px;
        }
        .mdc-button {
            width: 100%;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3f51b5;
            color: white;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .action-buttons {
            display: flex;
            gap: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Client File Download</h1>
        <label class="mdc-text-field mdc-text-field--outlined">
            <input type="text" id="date" class="mdc-text-field__input" placeholder="YYYY-MM-DD">
            <span class="mdc-notched-outline">
                <span class="mdc-notched-outline__leading"></span>
                <span class="mdc-notched-outline__notch">
                    <span class="mdc-floating-label">Choose a date</span>
                </span>
                <span class="mdc-notched-outline__trailing"></span>
            </span>
        </label>
        <label class="mdc-text-field mdc-text-field--outlined">
            <input type="text" id="ticker" class="mdc-text-field__input" placeholder="Enter Ticker Name">
            <span class="mdc-notched-outline">
                <span class="mdc-notched-outline__leading"></span>
                <span class="mdc-notched-outline__notch">
                    <span class="mdc-floating-label">Ticker Name</span>
                </span>
                <span class="mdc-notched-outline__trailing"></span>
            </span>
        </label>
        <button class="mdc-button mdc-button--raised" onclick="fetchData()">
            <span class="mdc-button__label">Get Data</span>
        </button>
       <table id="data-table">
            <thead>
                <tr>
                    <th>Download Action</th>
                    <th>Client Name</th>
                    <th>Index Ticker</th>
                    <th>Index Name</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>
    <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
    <script>
        mdc.textField.MDCTextField.attachTo(document.querySelector('.mdc-text-field'));
        mdc.ripple.MDCRipple.attachTo(document.querySelector('.mdc-button'));

        flatpickr("#date", {
            dateFormat: "Y-m-d",
            allowInput: true
        });

        function fetchData() {
            const date = document.getElementById('date').value;
            const ticker = document.getElementById('ticker').value;
            fetch(`/api/ftp/get-client-data?date=${date}&ticker=${ticker}`)
                .then(response => response.json())
                .then(data => {
                    const tableBody = document.getElementById('data-table').getElementsByTagName('tbody')[0];
                    tableBody.innerHTML = '';
                    const newRow = tableBody.insertRow();
                    newRow.innerHTML = `
                        <td class="action-buttons">
                            <button class="mdc-button mdc-button--outlined" onclick="downloadFile('Opening', '${data.tickerName}', '${date}','${data.clientName}')">Opening</button>
                            <button class="mdc-button mdc-button--outlined" onclick="downloadFile('Closing', '${data.tickerName}', '${date}','${data.clientName}')">Closing</button>
                        </td>
                        <td>${data.clientName}</td>
                        <td>${data.tickerName}</td>
                        <td>${data.datesCreated}</td>
                    `;
                })
                .catch(error => console.error('Error:', error));
        }


        function downloadFile(action, ticker, date, clientName) {
            // Creating File Name based on clicked values
            const fileName = `${action}-${ticker}-${date}`;

            console.log(`Downloading File ${fileName} for Client: ${clientName}`);
            // Add your FTP download logic here
            
        }
    </script>

</body>
</html>
```
### Modify the API, path

1. Add the file path to `<appName>/views.py`, so that it can be used to API redirection : **ftpFileDownload/views.py**
    ```python
        from rest_framework.views import APIView
        from rest_framework.response import Response
        from rest_framework import status

        # Import file from .serializers file 
        from .serializers import ClientInfoSerializer


        # Api Routing on what it will do 
        class GetClientInfoUsingTickerNameAndDate(APIView):

        #.......
            
        # To add frontend url
        from django.shortcuts import render

        def index(request):
            return render(request, 'index.html')
    ```

2. Now, we also need to define **index.html** path in app urls, so that it will be reachable

   - Go to **<appName>.urls.py** and the path: **ftpFileDownload.py**
    ```python
        from django.urls import path

        # Import the API that has been created, and configure the URLs
        from .views import GetClientInfoUsingTickerNameAndDate,index

        urlpatterns = [
            path('get-client-data/', GetClientInfoUsingTickerNameAndDate.as_view(), name='get-client-data'),
            path('', index, name='index'),
        ]
    ```

3. Run the server : `python manage.py runserver`
4. Go to : <hotname>/api/ftp/ -> for UI ```http://127.0.0.1:8000/api/ftp/```


## FTP to download the file

#### Modify the HTML, to update the downloadFile Logic


1. Modify the **javaScript** which will call the backend API to download the file

    ```javascript

        function downloadFile(action, ticker, date, clientName) {
                    // Creating File Name based on clicked values
                    const fileName = `${action}-${ticker}-${date}`;

                    console.log(`Downloading File ${fileName} for Client: ${clientName}`);
                    // Add your FTP download logic here
                    window.location.href = `/api/ftp/download/${fileName}/${clientName}/`;
                    
                }
    ```

    This is the whole file

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FTP</title>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">

        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #3f51b5;
            }
            .mdc-text-field {
                width: 100%;
                margin-bottom: 20px;
            }
            .mdc-button {
                width: 100%;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #3f51b5;
                color: white;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            .action-buttons {
                display: flex;
                gap: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Client File Download</h1>
            <label class="mdc-text-field mdc-text-field--outlined">
                <input type="text" id="date" class="mdc-text-field__input" placeholder="YYYY-MM-DD">
                <span class="mdc-notched-outline">
                    <span class="mdc-notched-outline__leading"></span>
                    <span class="mdc-notched-outline__notch">
                        <span class="mdc-floating-label">Choose a date</span>
                    </span>
                    <span class="mdc-notched-outline__trailing"></span>
                </span>
            </label>
            <label class="mdc-text-field mdc-text-field--outlined">
                <input type="text" id="ticker" class="mdc-text-field__input" placeholder="Enter Ticker Name">
                <span class="mdc-notched-outline">
                    <span class="mdc-notched-outline__leading"></span>
                    <span class="mdc-notched-outline__notch">
                        <span class="mdc-floating-label">Ticker Name</span>
                    </span>
                    <span class="mdc-notched-outline__trailing"></span>
                </span>
            </label>
            <button class="mdc-button mdc-button--raised" onclick="fetchData()">
                <span class="mdc-button__label">Get Data</span>
            </button>
        <table id="data-table">
                <thead>
                    <tr>
                        <th>Download Action</th>
                        <th>Client Name</th>
                        <th>Index Ticker</th>
                        <th>Index Name</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
        <script>
            mdc.textField.MDCTextField.attachTo(document.querySelector('.mdc-text-field'));
            mdc.ripple.MDCRipple.attachTo(document.querySelector('.mdc-button'));

            flatpickr("#date", {
                dateFormat: "Y-m-d",
                allowInput: true
            });

            function fetchData() {
                const date = document.getElementById('date').value;
                const ticker = document.getElementById('ticker').value;
                fetch(`/api/ftp/get-client-data?date=${date}&ticker=${ticker}`)
                    .then(response => response.json())
                    .then(data => {
                        const tableBody = document.getElementById('data-table').getElementsByTagName('tbody')[0];
                        tableBody.innerHTML = '';
                        const newRow = tableBody.insertRow();
                        newRow.innerHTML = `
                            <td class="action-buttons">
                                <button class="mdc-button mdc-button--outlined" onclick="downloadFile('Opening', '${data.tickerName}', '${date}','${data.clientName}')">Opening</button>
                                <button class="mdc-button mdc-button--outlined" onclick="downloadFile('Closing', '${data.tickerName}', '${date}','${data.clientName}')">Closing</button>
                            </td>
                            <td>${data.clientName}</td>
                            <td>${data.tickerName}</td>
                            <td>${data.datesCreated}</td>
                        `;
                    })
                    .catch(error => console.error('Error:', error));
            }


            function downloadFile(action, ticker, date, clientName) {
                // Creating File Name based on clicked values
                const fileName = `${action}-${ticker}-${date}`;

                console.log(`Downloading File ${fileName} for Client: ${clientName}`);
                // Add your FTP download logic here
                window.location.href = `/api/ftp/download/${fileName}/${clientName}/`;
                
            }
        </script>

    </body>
    </html>
    ```

2. In Serializer add the DTO to receive the input

- Go to `serializers.py` to create a model in **<appName>/serializers.py** : `ftpFileDownload/serializers.py`
    ```python
    from rest_framework import serializers

    class ClientInfoSerializer(serializers.Serializer):
        # Validations are also added for the format
        date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
        ticker = serializers.CharField(max_length=10)

    # This one 
    class FtpFileDownload(serializers.Serializer):
        # Validations are also added for the format
        fileName = serializers.CharField()
        clientName = serializers.CharField()

    

    ```

3. Modify the views.py to add the logic 

- Add import for Serializer : `from .serializers import ClientInfoSerializer, FtpFileDownload`

- Now add the API logic
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Import file from .serializers file 
from .serializers import ClientInfoSerializer, FtpFileDownload


# Api Routing on what it will do 
class GetClientInfoUsingTickerNameAndDate(APIView):

    # Get API
    def get(self, request, format=None):
        # Extracting the query parameter
        serializer = ClientInfoSerializer(data=request.query_params)

        # Validating If the parameters are correct
        if serializer.is_valid():

            
            data = {
                "clientName": "John Doe",
                "tickerName": serializer.validated_data['ticker'],
                "datesCreated": serializer.validated_data['date'].strftime('%Y-%m-%d')
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# To add frontend url
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')



# For downloading FTP Files 

import ftplib
from django.http import HttpResponse

class FTPDownloadView(APIView):
    def get(self, request, format=None):
        serializer = FtpFileDownload(data=request.query_params)

        if serializer.is_valid():
            clientName = serializer.validated_data['clientName']

            # FTP Related Data
            fileName = serializer.validated_data['fileName']
            ftp_directory = f'/path/to/files/{clientName}/'
            ftp_server = 'ftp.example.com'
            ftp_user = 'your_username'
            ftp_password = 'your_password'

            try:
                ftp = ftplib.FTP(ftp_server)
                ftp.login(user=ftp_user, passwd=ftp_password)
                ftp.cwd(ftp_directory)
                files = ftp.nlst()

                matching_files = [f for f in files if f.startswith(fileName)]
                if not matching_files:
                    return HttpResponse("File not found", status=404)

                file_to_download = matching_files[0]
                response = HttpResponse(content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_to_download}"'

                ftp.retrbinary(f"RETR {file_to_download}", response.write)
                ftp.quit()
                return response
            except ftplib.all_errors as e:
                return HttpResponse(f"FTP error: {str(e)}", status=500)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```