from flask import Flask, render_template, request
import hid
app = Flask(__name__)


# docs:
# http://steventsnyder.com/reading-a-dymo-usb-scale-using-python/
# https://trezor.github.io/cython-hidapi/

# terminal command to list usb devices: system_profiler SPUSBDataType


# Dymo IDs; both sets work
VENDOR_ID = 0x0922
PRODUCT_ID = 0x8003
# VENDOR_ID = 2338
# PRODUCT_ID = 32771


@app.route("/", methods=["GET", "POST"])
def home():
    weight = 0
    if request.method == 'POST':
        weight = str(get_weight())
    return render_template('index.html', weight=weight)


def get_weight():
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        data = device.read(64)
        print(data)
        weight = data[4]
        device.close()
        return weight
    except IOError as ex:
        print(ex)


if __name__ == "__main__":
    app.run(debug=True)