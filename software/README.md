# About
* This is the software section of the [LUFbot](https://github.com/sean-was-taken/LUFbot)
# Usage
* Once you have assembled the LUFbot according to the [Hardware Section](../hardware/), clone this repository and run with `$ python3 ./detection.py`
* If you find the tracking to be inaccurate, try tweaking the `min_conf_threshold` value and the `(ymax-ymin) * (xmax-xmin) < (1360*768/3) - 50000` lines. 

# Credits
* Work is based on [This repository from EdjeElectronics](/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi)
* Ira Pino [Email](mailto:ip6142@pleasantonusd.net)
* Xinle Yao [Email](mailto:xy2933@pleasantonusd.net) [GitHub](/sean-was-taken)
* Part of [PVA](https://www.pleasantonvirtualacademy.com) Coding Club, [PUSD](https://www.pleasantonusd.net)
