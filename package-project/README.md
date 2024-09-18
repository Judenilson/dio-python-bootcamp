# jd_image_process

Description. 
The package jd_image_process is used to:
	- Complete the requirements of a challenge in a Data Engineering class at Digital Innovation One.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install jd_image_process

```bash
pip install jd_image_process
```

## Usage

```python
from jd_image_process.utils import io, plot
from jd_image_process.processing import combination, transformation

image1 = io.read_image('image1_path')
image2 = io.read_image('image2_path')

plot.plot_image(image1)
plot.plot_image(image2)

result_image = combination.transfer_histogram(image1, image2)
plot.plot_result(image1, image2, result_image)
```

## Author
Judenilson Araujo
www.judenilson.com.br

## License
[MIT](https://choosealicense.com/licenses/mit/)