
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


if __name__ == '__main__':
	original = Image.open("ice_bear.jpg")
	original.load()
	#original.show()
	pic_width = original.size[0]
	pic_height = original.size[1]

	print "The size of the Image is: "
	print str(pic_width) + 'x' + str(pic_height)
	
	pixels = list(original.getdata())
	result_pic = ''
	for i in range(pic_width):
		for j in range(pic_height):
			pix = pixels[i*pic_width+j]
			if pix[0] >235 and pix[1] > 235 and pix[2] > 235:
				result_pic += ' '
			else:
				result_pic += '*'
		result_pic += '\n'
	print result_pic

	original.save("a_test.png")
