# TFM
TFM sobre generación de informes de árbitros en Python

# Versión de Python utilizada
**Python 3.12.9** --> He probado en el servidor con Python 3.13, pero esta puede generar problemas o incompatibilidades, especialmente con bibliotecas como sentencepiece, necesaria para los modelos.
Es necesario realizar la descarga de la versión 3.12.9.

# Entorno virtual
Una vez descargada la versión de Python, utilizarla para crear un entorno virtual con los siguientes comandos dentro del directorio TFM:
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

He probado a hacerlo manualmente y he eliminado algunas dependencias propias de Windows para Python que provocaban incompatibilidades.

# Instalar Ollama
En la máquina con el servidor Flask, he clonado el repositorio con los ficheros necesarios para el uso de la herramienta. Para utilizarla, solo hay que instalar Ollama en su versión 0.6.8, que es la que he utilizado para el TFM, aunque se puede probar con versiones más modernas.
Si quieres instalar la versión más moderna de Ollama, puedes usar el siguiente comando:
curl -fsSL https://ollama.com/install.sh | sh

O también puedes usar la instalación manual con:
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
sudo tar -C /usr -xzf ollama-linux-amd64.tgz

Para instalar la versión específica, puedes usar este comando:
curl -fsSL https://ollama.com/install.sh | OLLAMA_VERSION=0.6.8 sh

Para actualizar Ollama, ejecuta el comando de instalación más moderna o manual.
Una vez instalado, se abre un bash y usan los comandos:
Ejecución: 
ollama serve &

Descarga del modelo:
ollama pull gemma3:12b

Si tienes alguna duda de cómo realizar la instalación para Linux, te adjunto la dirección del documento github que lo explica:
https://github.com/ollama/ollama/blob/main/docs/linux.md

# Ejecución de la app
Para ejecutar la app, simplemente realizar la ejecución del main.py y se lanzará la app Flask. Abre en el navegador la ruta que se indique en la terminal y puedes usarlo.

Nota: En mi máquina Windows, el tiempo que tarda en generarse el resumen es de entre 15-30 segundos. He realizado estos mismos pasos en otra máquina Ubuntu y el despliegue es correcto, pero tarda un par de minutos en generar los resúmenes. No he averiguado si se debe al uso de Ollama en otro sistema operativo, la lentitud de mi máquina Ubuntu o algún motivo claro, por lo que es posible que ocurra un retraso notable en la generación de resúmenes.