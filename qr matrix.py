import sys

import numpy
from PIL import Image


class QRMatrix:
    
    type_of_encoding = {0 : "End", 1:"Numeric", 2:"Alphanumeric", 3:"Structred Append", 4:"Byte", 5:"FNC1 in First",
                        7:"Extended Channel Interpretation", 8:"Kanji", 9:"FNC1 in Second"}
    pad_bytes = {0 : 236, 1: 17}
    error_correction_levels = {3: "L", 1:"M", 2:"Q", 0:"H"}


    def __init__(self, decode_or_encode, image_or_text="", ):

        if decode_or_encode == "decode":
            self.matrix = numpy.asarray(Image.open(image_or_text).convert('L')).tolist()
            self.__trim_white_space()
            self.__scale_matrix()
            self.version = ((len(self.matrix) - 21) // 4) + 1
        elif decode_or_encode == "encode":
            print("Matrix Maker has not been implemented yet")

    def __str__(self):

        for row in self.matrix:
            print [i if i != 255 else 1 for i in row]
        return ""

    def __out_of_bounds(self, x, y):

        if x > len(self.matrix) - 1 or y > len(self.matrix) - 1:
            return True
        elif x < 0 or y < 0:
            return True
        elif x < 9 and (y < 9 or y >= len(self.matrix) - 8):
            return True
        elif x < 9 and y >= len(self.matrix) - 8:
            return True
        else:
            return False

    def __get_error_correction_level(self, traversal):


        return self.error_correction_levels[self.matrix[8][0] * 1 + self.matrix[8][1] * 2]
    def decode(self):

        zig_zag_traversal = self.__traverse_matrix()
        word = ""
        try:
            encoding_mode = self.type_of_encoding[self.__decode_bits(zig_zag_traversal, 0, 4)]
        except KeyError:
            print("Non-existing encode mode.")

        length = self.__decode_bits(zig_zag_traversal, 4)
        if encoding_mode == "Byte" or encoding_mode == "Japanese":
            bytes=8
            decode_function = chr
        elif encoding_mode == "Alphanumeric":
            bytes = 9
            #decode_function =
        elif encoding_mode == "Numeric":
            bytes=10
            #decode_function =
        else:
            raise Exception(encoding_mode + " has not yet been implemented")
        for i in range(length):
            word += decode_function(self.__decode_bits(zig_zag_traversal, 12 + i * bytes))
        return word

    def __within_orientation_markers(self, x, y):

        if self.version > 1:
            return x in range(len(self.matrix) - 10 + 1, len(self.matrix) - 5 + 1) and y in range(
                len(self.matrix) - 10 + 1, len(self.matrix) - 5 + 1)

    def __in_fixed_area(self, x, y):

        if self.__within_orientation_markers(x, y):
            return True
        elif x == 6 or y == 6:
            return True

    def __decode_bits(self, traversal, start, number_of_bits=8):

        factor = 2 << (number_of_bits - 2)
        character = 0
        for i in traversal[start:start + number_of_bits]:
            character += i * factor
            if factor == 1:
                return character
            factor /= 2

    def __traverse_matrix(self):

        traversal = []
        x, y, direction = len(self.matrix) - 1, len(self.matrix) - 1, -1
        matrix = self.__demask()
        while True:
            if self.__out_of_bounds(x, y):
                direction, y, x = -direction, y - 2, x - direction
            if not self.__in_fixed_area(x, y):
                traversal += [matrix[x][y]]
            if y < 8:
                break
            elif y % 2 != 0:
                x, y = x + direction, y + 1
            else:
                y -= 1
        return traversal

    def __demask(self):

        mask = self.__extractMaskPattern()
        decodedMatrix = []
        y = 0
        while y < len(self.matrix):
            row = []
            x = 0
            while x < len(self.matrix[0]):
                modifyValue = self.matrix[y][x]
                if (modifyValue == 255):
                    modifyValue = 1
                row += [(~modifyValue + 2 ^ ~mask[y][x] + 2)]
                x += 1
            decodedMatrix += [row]
            y += 1
        return decodedMatrix

    def encode(self):


        return

    def __extractMaskPattern(self):


        maskPattern = self.matrix[8][2:5]
        power = 1
        total = 0
        for i in maskPattern:
            if i == 0:
                total += power
            power <<= 1
        maskMatrix = []
        j = 0
        for row in self.matrix:
            i = 0
            newRow = []
            for val in self.matrix[j]:
                if self.__extractMaskNumberBoolean(total, i, j):
                    newRow += [0]
                else:
                    newRow += [1]
                i += 1
            j += 1
            maskMatrix += [newRow]

        return maskMatrix

    def __extractMaskNumberBoolean(self, number, j, i):

        if number == 0:
            return (i * j) % 2 + (i * j) % 3 == 0
        elif number == 1:
            return i % 2 == 0
        elif number == 2:
            return ((i * j) % 3 + i + j) % 2 == 0
        elif number == 3:
            return (i + j) % 3 == 0
        elif number == 4:
            return (i / 2 + j / 3) % 2 == 0
        elif number == 5:
            return (i + j) % 2 == 0
        elif number == 6:
            return ((i * j) % 3 + i * j) % 2 == 0
        elif number == 7:
            return j % 3 == 0
        else:
            raise Exception("Unknown Mask Pattern")

    def __trim_white_space(self):


        isUsefulRow = False
        trimmedMatrix = []
        startPoint, endPoint = 0, 0
        for row in self.matrix:
            if isUsefulRow:
                if len(trimmedMatrix) == endPoint - startPoint:
                    break
                trimmedMatrix += [row[startPoint: endPoint]]
            elif not self.__rowIsWhiteSpace(row):
                isUsefulRow = True
                startPoint, endPoint = self.__extract_end_points(row)
        self.matrix = trimmedMatrix

    def __extract_end_points(self, firstRow):

        wastedSpace = 0
        for num in firstRow:
            if num == 255:
                wastedSpace += 1
            else:
                break
        lastBlackIndex, count = wastedSpace, wastedSpace
        for num in firstRow[wastedSpace:]:
            if num == 0:
                lastBlackIndex = count
            count += 1
        return (wastedSpace, lastBlackIndex)

    def __rowIsWhiteSpace(self, row):

        for i in row:
            if i != 255:
                return False
        return True

    def __find_ratio(self, matrix):


        for row in matrix:
            scale = 0
            for num in row:
                scale += 1
                if num == 255:
                    return scale // 7
        raise Exception("This image is not binary!")

    def __scale_matrix(self):

        ratio = self.__find_ratio(self.matrix)
        scaledMatrix = []
        yCount = 0
        for row in self.matrix:
            if yCount % ratio == 0:
                xCount = 0
                newRow = []
                for value in row:
                    if xCount % ratio == 0:
                        newRow += [value]
                    xCount += 1
                scaledMatrix += [newRow]
            yCount += 1
        self.matrix = scaledMatrix


if __name__ == "__main__":
    QRCode = QRMatrix(sys.argv[1], sys.argv[2])
    print(QRCode.decode())