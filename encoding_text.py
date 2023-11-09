import base64
b = base64.b64encode(bytes('duleeka.roshinie@axiatadigitallabs.com:IROImdWyGxNPDqAuRfBVB2D7', 'utf-8')) # bytes
base64_str = b.decode('utf-8') # convert bytes to string
print(base64_str)