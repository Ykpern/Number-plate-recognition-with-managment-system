# Number-plate-recognition-with-managment-system

The Number Plate Recognition (NPR) with Management System is a comprehensive software solution designed to automate the process of vehicle identification and management. Leveraging advanced Optical Character Recognition (OCR) technology, the system captures and analyzes vehicle number plates in real time, providing accurate identification and logging of vehicle entries and exits.


## How it works

Implementation of the algorithm is written in Python using libraries opencv2 for image
operations, YOLO(You Only Look Once) for detecting the license plate and easyocr
for image to text and for user interface and graphical parts Tkinter by TkSoftware GUI
library and for the regular expression check Pythons regular expression module re  is
used. Python was chosen for its range of libraries and easy implementation for speed. Initially, although image operations were implemented with as less operations possible on the
CPU, it still showed to be insufficient in terms of the time it took to finish a complete analysis for relatively high resolution frames of license plates and a reimplementation of the same
algorithms on the GPU by utilizing the opencv library seemed to be necessary. This
library uses GPU when possible and increases the image operations by significant amount
compared to CPU based operations. For simplicity and test purposes, input files are limited
to .mp4 format.
Using one languages increases the utilization of I/O functions. Functions like Cropping
image, threshold, inverse, histogram equalization are called within the python code and executed through the GPU during the analysis.
For the user management part simple UI (figure 4.1) is designed for admin to manage
users.


<img width="635" alt="adminUI" src="https://github.com/user-attachments/assets/88346cfd-b3cf-4d9c-85e6-5d0a1e45c2b7">

Admin has a button at the top left which opens the entrance log (figure 4.2). At the same
time security can access this UI windows as well. It displays which vehicles get in the area
from last vehicle to first vehicle. It gets the data from database entrance table. Data in this
figure 4.2 is for the testing purposes names and license plates are not real and this doesn’t
represent any entrance of an area at that given time.


<img width="433" alt="securtiy" src="https://github.com/user-attachments/assets/a608a78e-a26c-439a-a824-e1dfba13c260">

Admin can add or replace users by their name, surname, apartment no and license plate
number but for delete operation only license plate is needed after clicking delete button.
System will check if any user exist with that number plate with this query:
25
SELECT * FROM plateTable WHERE licensePlate = %s
and if the user exist a new window will pop up (figure 4.3) with the users all information
for admin to confirm delete operation.

<img width="337" alt="deleteconfirm" src="https://github.com/user-attachments/assets/4b2678bf-0642-47fc-b3e7-37db93020069">

If the admin confirms the delete operation this query will be send to database to log the
operation same applies for the replace button all deleted and replaced users will end up in
this table.
INSERT INTO delete_log ( date, isim, soyisim, plaka, operation)
VALUES(%s, %s, %s, %s, %s)
A process of the implementation of how the database works with the license plate recognition algorithm is shown Figure 4.4

![imple](https://github.com/user-attachments/assets/fbe59c8f-2b3a-48f6-8543-c71495bc270c)

## License Plate Format Check With Regex
This program only works with Turkish license plates. Turkish license plates has 6 formats:

•N: Number || L: Letter

• NN L NNNNN (for police, etc. cars)

• NN L NNNN

• NN LL NNNN

• NN LL NNN

• NN LLL NNN

• NN LLL NN

To check if the read text’s format is Turkish license plate, this regular expression is used:

(0[1-9]|[1-7][0-9]|8[01])((\s?[a-zA-Z]\s?)(\d{4,5})|
(\s?[a-zA-Z]{2}\s?)(\d{3,4})|(\s?[a-zA-Z]{3}\s?)(\d{2,3}))

This regex first checks the 2 digits of the LP. If the digits are between 01-81 then it checks the
letter count with the corresponding digit count to make sure the format of the license plate is
correct

##  Database
For the storing the data part system uses MySQL which is an Oracle based open source
database management system.
MySQL provides numerous advantages, making it a preferred choice for many developers and organizations. As an open-source and free database management system, it offers a
cost-effective solution for development. MySQL’s scalability allows it to efficiently manage
both small and large databases, while its high performance ensures quick data access and
fast query processing. With support for various storage engines, MySQL offers flexibility to
users. Its robust security features, such as user authentication and data encryption, enhance
data protection. MySQL is also user-friendly, featuring a simple syntax and intuitive interface suitable for both beginners and advanced users. Additionally, it supports cross-platform
deployment, running seamlessly on Windows, Linux, and macOS. Which makes the implementation of the license plate software available on every OS. The extensive community
support, coupled with integration capabilities with numerous programming languages and
web development frameworks, further enhances its versatility. Renowned for its reliability and stability, MySQL consistently maintains data integrity and performance, making it a
reliable choice for a wide range of applications.

