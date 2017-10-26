Deploying to Heroku
------

1. Signup for [Heroku](https://api.heroku.com/signup)
2. Login to Heroku and download the [Heroku Toolbelt](https://toolbelt.heroku.com/)
3. Once installed, open your command-line and run the following command - `heroku login`. Then follow the prompts:

  ```
  Enter your Heroku credentials.
  Email: your_email@your.address
  Password (typing will be hidden):
  Could not find an existing public key.
  Would you like to generate one? [Yn]
  Generating new SSH public key.
  Uploading ssh public key e.g. /Users/your_user_name/.ssh/id_rsa.pub
  ```

4. Activate your virtualenv
5. Heroku recognizes the dependencies needed through a *requirements.txt* file. Create one using the following command: `pip freeze > requirements.txt`. Now, this will only create the dependencies from the libraries you installed using pip. If you used easy_install, you will need to add them directly to the file.
6. Create a Procfile. Open up a text editor and save the following text in it:

  ```
  web: gunicorn app:app --log-file=-
  ```

   Then save the file in your applications root or main directory as *Procfile* (no extension). The word "web" indicates to Heroku that the application will be attached to the HTTP routing stack once deployed.

7. Create a local Git repository (if necessary):

  ```
  $ git init
  $ git add .
  $ git commit -m "initial files"
  ```

8. Create your app on Heroku:

  ```
  $ heroku create <name_it_if_you_want>
  ```

9. Deploy your code to Heroku:

  ```
  $ git push heroku master
  ```

10. View the app in your browser:

  ```
  $ heroku open
  ```

11. Having problems? Look at the Heroku error log:

  ```
  $ heroku logs
  ```