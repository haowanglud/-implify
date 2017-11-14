from PIL import Image
import pytesseract as pya
import sys

pya.pytesseract.tesseract_cmdtesseract_cmd = '/usr/local/Cellar/tesseract/3.05.01/bin/tesseract'
# Include the above line, if you don't have tesseract executable in your PATH
# Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

def read_image_text(image):
	im = Image.open(image)
	string = pya.image_to_string(im)
	return string

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_digit(s, index):

	if s[index].isdigit() or s[index] == ' ' or s[index] == '.':
		# space must be next to .
		if s[index] == ' ' and ((index < len(s)-1 and s[index+1] == '.') or (index > 0 and s[index-1] == '.')):
			return True
		elif s[index] != ' ':
			return True
		else:
			return False
	return False


def grab_amount(row):
	size = len(row)
	num_list = []
	i = 0
	while i < size:
		num = ""
		index_of_decimal = 0
		is_spending = False;
		while i < size and is_digit(row, i):
			# ignore space in the amount
			if row[i] != ' ':
				num+=row[i]
			if row[i] == '.':
				index_of_decimal = len(num)
			i += 1

		# if num is a valid number and has two decimal precision ($xx.xx)
		if num != "":
			print('--------')
			print('num: {2}, len: {0},  decimal: {1}'.format(len(num), index_of_decimal, num))
			print('--------')
		if is_number(num) and len(num)-index_of_decimal == 2 and index_of_decimal != 0:
			num_list.append(float(num))
		i+=1

	return num_list

def process_text(string):
	num_list = []

	# add all amounts into the list
	num_list = grab_amount(string)

	print(num_list)
	total = -1
	try:
		total = max(num_list)
	except:
		print("No vaild spending recognized")

	return total

def parse_arg():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
	ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
	args = vars(ap.parse_args())
	return args

if __name__ == "__main__":
	if len(sys.argv) <= 3:
		print("Usage: python3 main --image imagename --preprocess processmethod")
		exit(1)



#	string = read_image_text(sys.argv[1])
	print(string)
	total_spending = process_text(string)
	print(total_spending)