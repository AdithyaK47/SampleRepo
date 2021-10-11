import csv
import cv2
import imutils
import logging
import os
import time

startTime = time.time()

file = open("Paths.txt", "r")
source_path = file.readline().rstrip("\n").split("=")[1]
target_path = file.readline().rstrip("\n").split("=")[1]
result_path = file.readline().split("=")[1]

os.chdir(source_path)
filenames = os.listdir(os.getcwd())

fields = ["Page_Filename", "Status"]
myList = []

for i in filenames:
    source = os.path.join(source_path, i)
    target = os.path.join(target_path, i)

    flag = True

    if os.path.isfile(target):
        org = cv2.imread(source)
        new = cv2.imread(target)

        diff = org.copy()
        cv2.absdiff(org, new, diff)

        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        for b in range(0, 3):
            dilated = cv2.dilate(gray.copy(), None, iterations=b + 1)

        (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

        contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(new, (x, y), (x + w, y + h), (0, 0, 255), 2)
            flag = False

        if flag:
            result = os.path.join(result_path, "Success")
            status = "Pass"
        else:
            result = os.path.join(result_path, "Fail")
            status = "Fail"

        if not os.path.isdir(result):
            os.mkdir(result)

        result = os.path.join(result, i)
        cv2.imwrite(result, new)

        dictionary = {"Page_Filename": os.path.splitext(i)[0], "Status": status}
        myList.append(dictionary)

    else:
        logger = logging.getLogger(__name__)
        log = os.path.join(result_path, "record.log")
        logging.basicConfig(filename=log, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f"File {i} missing at target")


csv_result = os.path.join(result_path, "Records.csv")

with open(csv_result, 'w', newline='') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(myList)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
print("Hey")
print("Hello")
