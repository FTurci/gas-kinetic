# Collisional dynamics

A minimal Bokeh application rendering the kinetic gas dynamics.



## Deployment on Render.com



- Follow the file structure of the branch, i.e.:

  ```
  - .
  - src/main.py
  - requirements.txt
  ```

- To produce the `requirements.txt`  file, use the python utility `pipreqs`. 

  You can install it via

  ```
  pip install pipreqs
  ```

  and use it as
  ```
  pipreqs src/main.py 
  ```

  Remember to ove the `requirements.txt` file to the root directory

  ```
  mv src/requirements.txt .
  ```

- When configuring the Render application:

  - build command type: `pip install -r requirements.txt`
  - start command: `bokeh serve --num-procs=0 --allow-websocket-origin=kinetic-gas.onrender.com --address=0.0.0.0 --use-xheaders src/main.py`

  

- 
