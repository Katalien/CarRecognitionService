## Video Capture Car Detection task
A web service for detecting cars in video captures using the YOLO model.

### How to use

1. Clone the repository:
```
git clone https://github.com/Katalien/CarRecognotionService.git
```
2. Navigate to the cloned repository folder:
```commandline
cd CarRecognotionService
```
3. Build the Docker container:
```commandline
docker build -t car_service .
```
4. Run the service on a specific host:
```commandline
docker run -p 8000:8000 car_service
```
5. Open the service in a browser:
go to http://localhost:8000 to use the service.