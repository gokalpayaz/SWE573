docker-compose build
# this will build with the tag specified in compose file. makes sense to increment.
docker login swe573registry.azurecr.io
# login with azure registry creds
docker tag swe573:1.0 swe573registry.azurecr.io/swe573:1.0
# it will look like there is another image with the same id but actually
# it is the same image with different id. this is expected.
docker push swe573registry.azurecr.io/swe573:1.0
