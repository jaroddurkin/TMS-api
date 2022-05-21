# API Reference

# GET /health

This endpoint is a basic health-check to get the status of your running API, as well as the current ping time to the website.

# GET /{TERM}/{CLASS}

This will get basic info on all class offerings for a particular class in a term.

**Path Parameters**
- Term
    - Indicates the term that you are searching for classes in
    - Example: WI21 = (Winter Term 2021-2022 Year), SU20 = (Summer Term 2020-2021 Year)
    - The year indicates the start of the academic year.
- Class
    - Indicates the specific class ou want to search for sections of.
    - Example: CS260, SE181
    - This should be the full class code like above.

**Query Parameters**
- method
    - Filters classes returned based on instructional method
    - Options: f2f, hybrid, async, sync, online
- prof
    - Filters classes based on primary professor
    - String has to match exactly the way the TMS website displays.
- full
    - Filters classes if they are full or not.
    - Boolean parameter.

**Response**

Returns a list of JSON objects that indicate each possible section of the class, with the following properties:

- type: Lecture, Lab, Recitation, etc.
- method: Instructional method such as Face to Face.
- sec: The section number of the class
- crn: The Drexel CRN for this class
- full: Boolean if the class is full or not
- prof: The primary professor for the class
- time: The day of the week + time of each class

# GET /{TERM}/{CLASS}/details

This gets extra info, along with everything from the previous endpoint. These are separated because it uses another API call to get the extra information like number of seats, location, etc.

**Path Parameters**
- Term
    - Indicates the term that you are searching for classes in
    - Example: WI21 = (Winter Term 2021-2022 Year), SU20 = (Summer Term 2020-2021 Year)
    - The year indicates the start of the academic year.
- Class
    - Indicates the specific class ou want to search for sections of.
    - Example: CS260, SE181
    - This should be the full class code like above.

**Query Parameters**
- method
    - Filters classes returned based on instructional method
    - Options: f2f, hybrid, async, sync, online
- prof
    - Filters classes based on primary professor
    - String has to match exactly the way the TMS website displays.

**Response**

Returns a list of JSON objects that indicate each possible section of the class, with the following properties:

- type: Lecture, Lab, Recitation, etc.
- method: Instructional method such as Face to Face.
- sec: The section number of the class
- crn: The Drexel CRN for this class
- full: Boolean if the class is full or not
- prof: The primary professor for the class
- time: The day of the week + time of each class
- cred: Number of credits for the class
- campus: Campus that this class is located in
- seats: Total number of seats in the class
- enroll: Number of students currently enrolled
- avail: Number of seats available in section
- text: Any special comments Drexel provides for the class
- build: The building where the class is located
- room: The room number where the class is located
