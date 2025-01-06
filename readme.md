mfw hosting an image

**how-to:**

    podman build -t slash-wallpaper .
then

    podman run --detach --name slash-wallpaper -p 8000:8000 localhost/slash-wallpaper
you can use docker, syntax is the same anyway

after running the container, open it via nginx or other reverse-proxy thingy, example nginx config is located in [nginx-configs](https://github.com/nyorf/slash-wallpaper/tree/master/nginx-configs)

![showcase.gif](showcase.gif?raw=true)
