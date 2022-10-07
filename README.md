# APP-COMPLIANCE
## Aplicacion de escritorio, para la soluciones de ISSUES Compliance.

- Descargar APPCompliance.zip.

- Descomprimir en /home/$USER, se debe descomprimir la carpeta llamda APPCompliance y su contenido dentro de tu /home/, example : ***/home/$USER/APPCompliance/***

> NOTA : $USER, es la variable de tu usuario.

- Redirecionar : 
```
	cd /home/$USER/APPCompliance/  
```

- Dar permisos de ejecucion al ejecutable `APPCompliance`
```
	chmod +x APPCompliance
```

## Para LINUX

- Mover estos ficheros, para crear un lanzador .desktop.
	```
	sudo mv scripts/APPCompliance.desktop /usr/share/applications/
	sudo mv scripts/APPCapture.desktop /usr/share/applications/
	sudo cp images/APPCompliance.png /usr/share/pixmaps/
	sudo cp images/APPCapture.png /usr/share/pixmaps/
	```

- Ahora simplemente buscar la app, ya sea por su nombre APPCompliance, o compliance, app o issues


![img_compliance](https://user-images.githubusercontent.com/86171869/166647737-00522195-5d1d-4c40-a400-d29dab098291.png)
