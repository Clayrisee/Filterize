# Filterize

A simple Web aplication for applying filter to your selfie images. This web app contains 2 filter:
- Cartoonize : Filter that will return your cartoon selfie image
- Nose filter : Filter to replace your nose with animal nose (dog, cat, and pig)

### HOW TO USE

```
git clone https://github.com/Clayrisee/Filterize.git
```

Build the docker image 
```
docker build -t filterize:latest .
```

Run the container
```
 docker run -d -p 5000:5000 filterize:latest 
```
