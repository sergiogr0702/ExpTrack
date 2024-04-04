<p align="center">
</p>
<p align="center">
    <h1 align="center">ExpTrack</h1>
</p>
<p align="center">
		<em>Django Full Stack application for managing books expenses.</em>
</p>
<p align="center">
	<a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python"></a>
	<a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django"></a>
   <a href="https://getbootstrap.com"><img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap"></a>
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Getting Started](#-getting-started)
  - [ Pre-Requisites](#-pre-requisites)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Commands](#-commands)
- [ Development](#-development)
  - [ Development Environment](#-development-environment)
  - [ Build](#-build)
  - [ Deployment](#-deployment)
- [ Contributing](#-contributing)
- [ Gallery](#-gallery)
- [ License](#-license)
</details>
<hr>

##  Overview

<p align="justify">
   ExpTrack is a simple but complete expense tracker application to manage the expenses of books. It is build using the Django Full Stack framework. This web application offers a variety of views for creating, viewing and editing books. Between these views you can find JQuery tables and different types of charts for the visualization of the data. The app also incorporates authentication and authorization to access the different views available.
   One main feature that this application has that differenciates it from other projects is the ability to create books and categories from an Excel file with the requiered fields in the correct format. To know the required format you can visit the example data available at 'demo-project' folder in the project source code.
</p>

---

##  Getting Started

In the next sections the requirements and installation instructions can be found:

### Pre-Requisites
To execute the application, you need to install in your system the next tools:
- At least Python 3.8.0

### Installation
 1. Clone the ExpTrack repository:
```console
$ git clone https://github.com/sergiogr0702/ExpTrack.git
```

2. Change to the project directory:
```console
$ cd ExpTrack
```

3. Install the dependencies:
```console
$ pip install -r requirements.txt
```

4. Create the database migrations:
```console
$ python manage.py makemigrations
```

5. Run the migrations:
```console
$ python manage.py migrate
```

6. Create the admin user for the application:
```console
$ python manage.py createsuperuser
```

### Usage
To execute the project you need to go to the source folder and run the next command:

```console
$ python manage.py runserver
```

### Commands
In this subsection some of the most interesting commands that are offered in the Django framework are presented:

| Command | Description |
| --- | --- |
| `python manage.py runserver` | Starts the Django development server at http://127.0.0.1:8000/. This is the most basic command to run your Django application. |
| `python manage.py makemigrations` | Generates a new migration file that describes the changes to the database schema. This is the first step before applying the changes to the database. |
| `python manage.py migrate` | Applies the pending migrations to the database. This command is used after running `makemigrations` to apply the changes to the database schema. |
| `python manage.py createsuperuser` | Creates a new superuser account for the Django admin interface. This is useful for creating an account with full access to the application. |
| `python manage.py shell` | Opens an interactive Python shell where you can interact with your Django application. This is useful for testing code and performing ad-hoc queries. |
| `python manage.py test` | Runs the test suite for your Django application. This is an important command to ensure that your application is working as expected. |
| `python manage.py collectstatic` | Collects all the static files (like CSS, JavaScript, and images) and copies them to the `static` directory in your project. This is useful for serving static files in a production environment. |

## Development
In order to deploy this project online, some configurations and commands are required to be run before:


### Development Environment
Before building the project you need to set the following environment variables in the configuration file inside the settings.py file in djangoproj folder:
- ALLOWED_HOSTS

### Build
To generate a production-ready build for the ExpTrack project, follow these steps:

1. **Create a Production-Ready Settings File**: In the ExpTrack/settings/ directory, create a new file called prod.py. This file will contain the settings for your production environment.

2. **Configure the Database**: In the prod.py file, configure the database settings for your production environment. You can use a service like PostgreSQL or MySQL.

3. **Configure the Static Files**: In the prod.py file, configure the settings for serving static files in your production environment. You can use a service like AWS S3 or Google Cloud Storage.

4. **Set Up a WSGI Server**: To serve your Django application in a production environment, you need to set up a WSGI server. You can use a service like Gunicorn or uWSGI.

5. **Create a New Branch**: Create a new branch in your Git repository specifically for your production-ready build. This will allow you to keep your production environment separate from your development environment.

6. **Install Dependencies**: Install the dependencies listed in the requirements.txt file by running:
   ```console
   $ pip install -r requirements.txt
   ```

7. **Run Migrations**: Before you can run the project, you need to create the necessary database tables. To do this, run the following command:
   ```console
   $ python manage.py makemigrations
   ```

8. **Apply Migrations**: After running makemigrations, apply the changes to the database by running:
   ```console
   $ python manage.py migrate
   ```

9. **Create a Superuser**: To create a superuser account for the Django admin interface, run:
   ```console
   $ python manage.py createsuperuser
   ```

10. **Collect Static Files**: Collect all the static files (like CSS, JavaScript, and images) and copy them to the static directory in your project. This is useful for serving static files in a production environment. To do this, run:
      ```console
      $ python manage.py collectstatic
      ```

11. **Run the Project**: Finally, run the project by executing:
      ```console
      $ python manage.py runserver
      ```

12. **Test Your Application**: Before deploying your application, test it thoroughly to ensure that it is working as expected. You can use a service like Selenium or Postman to automate your testing process.

13. **Deploy Your Application**: Once you have tested your application and are satisfied with its performance, you can deploy it using a service like Heroku, AWS Elastic Beanstalk, or Google App Engine.

14. **Monitor Your Application**: After deploying your application, monitor its performance using a service like New Relic or Datadog. This will help you identify and fix any issues that may arise in your production environment.

### Deployment
To deploy your production-ready build of the ExpTrack project online, follow these steps:

1. **Choose a Hosting Platform**: There are several hosting platforms available that you can use to deploy your Django application. Some popular options include Heroku, AWS Elastic Beanstalk, and Google App Engine. Choose the platform that best suits your needs and budget.

2. **Set Up Your Hosting Environment**: Once you have chosen a hosting platform, set up your hosting environment according to the platform's documentation. This may involve creating a new account, installing the necessary software, and configuring your application's settings.

3. **Push Your Code to a Remote Repository**: Before you can deploy your application, you need to push your code to a remote repository. This can be done using a service like GitHub, GitLab, or Bitbucket. Create a new repository for your project and push your code to it using the following command:
   ```console
   $ git push origin <your-branch-name>
   ```

4. **Deploy Your Application**: Once you have pushed your code to a remote repository, deploy your application using the hosting platform's deployment process. This may involve running a deployment command, creating a new application instance, or uploading a deployment package.

5. **Configure Your Domain Name**: If you want to use a custom domain name for your application, you will need to configure your domain's DNS settings to point to your hosting platform's servers. This can be done using the hosting platform's domain configuration tools.

6. **Monitor Your Application**: After deploying your application, monitor its performance using a service like New Relic or Datadog. This will help you identify and fix any issues that may arise in your production environment.

7. **Update Your Application**: As your application evolves, you will need to update it regularly to ensure that it remains secure and functional. To do this, follow the same process that you used to create your production-ready build: create a new branch, make your changes, test your application, and deploy it to your hosting platform.

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/sergiogr0702/ExpTrack/issues)**: Submit bugs found or log feature requests for the `ExpTrack` project.
- **[Submit Pull Requests](https://github.com/sergiogr0702/ExpTrack/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/sergiogr0702/ExpTrack/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/sergiogr0702/ExpTrack
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/sergiogr0702/ExpTrack/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=sergiogr0702/ExpTrack">
   </a>
</p>
</details>

---

##  Gallery
In this section you can find some examples of the application running:

- Login:

![Login]

- Register

![Register]

- Profile

![Profile]

- Dashboard

![Dashboard]

- Create book

![Create-book]

- Create category

![Create-category]

- Books table

![Books-table]

- Categories table

![Categories-table]

- Books import

![Book-import]

- Categories import

![Category-import]

- Report 1

![Report-1]

- Report 2

![Report-2]

- Report 3

![Report-3]

- Report 4

![Report-4]

---

##  License

This project is protected under the [Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/) License. For more details, refer to the [LICENSE](https://github.com/sergiogr0702/ExpTrack/blob/main/LICENSE/) file.


[**Return**](#-overview)

---

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Login]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/login.png
[Register]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/register.png
[Dashboard]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/dashboard.png
[Profile]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/profile.png
[Create-book]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/create_book.png
[Create-category]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/create_category.png
[Books-table]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/books_table.png
[Categories-table]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/categories_table.png
[Books-import]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/book_import.png
[Categories-import]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/category_import.png
[Report-1]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/report_1.png
[Report-2]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/report_2.png
[Report-3]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/report_3.png
[Report-4]: https://github.com/sergiogr0702/ExpTrack/blob/main/demo-images/report_4.png