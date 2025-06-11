![Screenshot 2025-06-11 174638](https://github.com/user-attachments/assets/5c936744-5ac0-42bf-b8ca-4a1f055460d1)
# GeoJSON Cleaner Dashboard

A prototype of [Streamlit app](https://geojson-cleaner.streamlit.app/) for automated cleaning and geometry fixing of GeoJSON files and previewing on a leaflet map.

---

## Features

- **Upload** a GeoJSON file.
- **Clean** it by removing invalid features or properties.
- **Explore logs** with transparent, user-friendly error reporting.
- **Preview** the cleaned GeoJSON on a map.
- **Download** the cleaned version.

---

##  Project Index
<table>
<tr>
    <td><b><a href='https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard/blob/master/dashboard.py'>dashboard.py</a></b></td>
    <td><code>❯ Main Streamlit app script, handles page layout, file upload, shows logs, attribute tables, map preview and download button</code></td>
</tr>
<tr>
    <td><b><a href='https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard/blob/master/utils.py'>utils.py</a></b></td>
    <td><code>❯ Helper functions for fixing GeoJSON geometries, performing validation, removing duplicates and creating a folium map</code></td>
</tr>
<td><b><a href='https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard/blob/master/Farm_file.geojson'>Farm_file.geojson</a></b></td>
    <td><code>❯ Sample input GeoJSON file</code></td>
<tr>
    <td><b><a href='https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard/blob/master/sample_output.geojson'>sample_output.geojson</a></b></td>
    <td><code>❯ Sample of a cleaned GeoJSON file produced by the app</code></td>
</tr>
<tr>
    <td><b><a href='https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard/blob/master/requirements.txt'>requirements.txt</a></b></td>
    <td><code>❯ List of all needed Python dependencies</code></td>
</tr>
<tr>
    <td><b><a href='https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard/blob/master/Dockerfile'>Dockerfile</a></b></td>
    <td><code>❯ Instructions for building a Docker container image</code></td>
</tr>
</table>

---

## 🚀 Installation & Running

1. Clone the repo
   ```bash
   git clone https://github.com/viktor-ko/GeoJSON_Cleaner_Dashboard.git
   cd GeoJSON_Cleaner_Dashboard
    ```
2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```
3. Install dependencies
    ```bash
   pip install -r requirements.txt
    ```
3. Run the Streamlit app
    ```bash
   streamlit run dashboard.py
    ```
    Open http://localhost:8501 in your browser.

## 🐳Docker Containerization📦

To containerize the Streamlit app using Docker on a Windows machine, follow these steps:

### 1️⃣ Install Docker Desktop

Download it here: https://www.docker.com/get-started  
Run it after installation — you can skip the account creation if you don’t need Docker Hub.

---

### 2️⃣ Create a `requirements.txt` file  
List all required Python packages with versions. For this app:

```ini
folium==0.19.5
geopandas==1.0.1
shapely==2.0.7
streamlit==1.44.0
streamlit_folium==0.24.0
```
---

### 3️⃣ Create a `Dockerfile`  
This file contains instructions to build the Docker image.

**Dockerfile**
```dockerfile
FROM python:3.13-slim
WORKDIR /dashboard
COPY dashboard.py utils.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["bash", "-c", "echo 'Use this URL: http://localhost:8501' && streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0"]
```

**Explanation:**
- `FROM` — base image, use a smaller version of Python 3.13 to reduce the Docker image size.
- `WORKDIR` — container working directory  
- `COPY` — copy app files and requirements.txt into container. `./` refers to the current directory  
- `RUN` — install Python packages. `--no-cache-dir` ignores packages cache, which reduces Docker image size  
- `EXPOSE` — open port 8501 (Streamlit default)  
- `CMD` — run the app and print access URL

---

### 4️⃣ Create a `.dockerignore` file (optional)  
If you're using PyCharm or other IDEs, exclude `.idea` or other unneeded folders:

```
.idea
```

---

### 5️⃣ Build the Docker image  
Run in terminal where your `Dockerfile` is:

```bash
docker build -t geojson-dashboard .
```
`.` at the end - current directory.
If it built successfully, you should see the message`FINISHED`in the terminal.

---

### 6️⃣ Verify the Docker image  

```bash
docker images
```
List all Docker images on your machine. You should see `geojson-dashboard` in the list of images.

---

### 7️⃣ Run the Docker container  

```bash
docker run -p 8501:8501 geojson-dashboard
```

Now open [http://localhost:8501](http://localhost:8501) in your browser.

---

### 8️⃣ Save the Docker image to a `.tar` file  

```bash
docker save -o geojson-dashboard.tar geojson-dashboard
```

---

### 📦 Load the image on another machine

Copy the `.tar` file to the target machine, then run:

```bash
docker load -i geojson-dashboard.tar
```

And start the container:

```bash
docker run -p 8501:8501 geojson-dashboard
```

---

### ✅ Done

That’s it — GeoJSON Cleaner Dashboard is containerized and portable!

