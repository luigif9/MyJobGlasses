# HOWTO Setup

## Dependencies

### OS Libraries

On Amazon Linux, several libraries need to be installed, you should be good with

        sudo yum -y install gcc-c++ python27-devel atlas-sse3-devel lapack-devel freetype-devel libpng-devel

### Python libraries

*Using pip virtualenv*

Code was re-tested using pip virtualenv. A venv folder can be created to store python dependencies

	pip install virtualenv
	virtualenv venv

Spawn a venv shell using

	source venv/bin/activate

From here you'll have loaded an isolated python shell
You can download all the libraries using

	pip install -r requirements.txt

*updating dependencies*

If you need to install additional libraries, please only do it from the virtualenv. Just source the venv bin like above. You can the run `pip install xxx` as usual

At the end, to record the new list of dependencies, while still inside the venv shell please issue

	pip freeze > requirements.txt

## Configuration

Boto3 and aws should be configured in order to have access to the AWS S3 server.
To configure these module, use the ```aws configure```command (http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

The file structure should follow this GitHub's structure and a temp folder should be added in the main folder (~/temp, in order to save the files downloaded from AWS).

# HOWTO Run

**Input**

This algorithm fetches the latest version of database exports (events file and blacklist files) directly on AWS S3 in myjobglasses-recommendation/ready/.

These files are then saved on in a temp folder.

**Usage**

call "main.py [-h] [-r] [-nb PREDICTIONNUMBER] [-u]" in order to compute recommendations

*Output* : recommandation.json file in the temp folder. This file can be directly uploaded on AWS S3 using the -u argument.

*optional arguments* :

  -h, --help            show this help message and exit

  -r                    Download a new version of events.json file

  -nb PREDICTIONNUMBER  Set the maximum number of prediction for each user.
                        Default = 2

  -u                    upload the recommendation.json file to AWS

call "export_history.py" in order to export user's history file.

*Output* : output_history.json file in the temp folder.

*Optional arguments* : None

