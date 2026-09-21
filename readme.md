mfw hosting an image

![showcase.gif](showcase.gif?raw=true)

**how-to:**

    podman build -t slash-wallpaper .
then

    podman run --detach --name slash-wallpaper -p 8000:8000 localhost/slash-wallpaper
you can use docker, syntax is the same anyway

after running the container, open it via nginx or other reverse-proxy thingy, example nginx config is located in [nginx-configs](https://github.com/nyorf/slash-wallpaper/tree/master/nginx-configs)

on dexter it runs from the ghcr.io/nyorf/hello-dexter image the workflow builds on every push to master; flux rolls the new tag out by itself
