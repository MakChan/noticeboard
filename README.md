# noticeboard


### About

Website for posting notices or any other information by college/school/organization staff for the students/employees.

Written in Django.

### Features
* Administrators/teachers can sign in and post notices.
* Students can view notices.
* Individual page for each notice.
* View notices by tags/categories.
* View all notices by a teacher.
* Notices can be written in markdown.
* Responsive design.



## How to setup

1. Install Python 3.6, Git and [Virtualenv] in your computer.

2. Get the source code on your machine.

    `git clone https://github.com/MakChan/noticeboard.git`

3. Create a Python virtual environment and install Python and Django related dependencies.

    ```shell
    cd noticeboard
    virtualenv venv # create virtual env
    venv\scripts\activate  # run this command everytime before starting on the project
    pip install -r requirements.txt
    ```

5. For running the server
   
    `python manage.py runserver`

6. Open the browser and go to to the following link.

    `http://127.0.0.1:8000/`


[virtualenv]: https://virtualenv.pypa.io/

