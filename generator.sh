#!/bin/bash
# Requirements: Assumes Python3.6, Django 2.0.0, and Git
# Requirements: Assumes Python3.6, PIP, Django 2.0.0, and Git
# A handy script for creating Django Projects and their respective applications
# Give this file `755` permissions in order to be able to run it.
# Usage: ./generator.sh PROJECT_NAME [APP_NAMES]



SITE=$1
firstapp=$2
secondapp=$3
thirdapp=$4
fourthapp=$5
CUR_DIR=$PWD



# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------



print_usage()
{
  echo "generator: Creates a django project and its specified apps."
  echo "usage: generator PROJECTNAME [APP names]"
}

print_help()
{
  echo "generator: Generates a django project directory with all the necessay files and subdirectories."
  echo "           The setup makes and commits migrations to the database as well as enables a .git repository."
  echo "           At the end of the setup, a server is also run on port 3009."
}


# ----------------------------------------
# ----------------------------------------
# ----------------------------------------


make_main()
{
  echo "$1"
  django-admin startproject $SITE
  cd $SITE

  echo "Updating urls..."
  sed -i 's/\]/\] \# \+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)/' $PWD/$SITE/urls.py
  cat $CUR_DIR/Templated/urls.txt >> $PWD/$SITE/urls.py

  echo "Updating settings..."
  cat $CUR_DIR/Templated/settings.txt >> $PWD/$SITE/settings.py
  sed -i 's/\: \[\]/: [os.path.join(BASE_DIR, "_templates_")]/' $PWD/$SITE/settings.py
}

make_static()
{
    cp $CUR_DIR/Templated/requirements.txt $PWD
    cp $CUR_DIR/Templated/_libraries_/*.py $PWD
    echo "Copied importable libraries."
    echo ""

    mkdir _media_
    cp -r $CUR_DIR/Templated/_sta* $PWD
    cp -r $CUR_DIR/Templated/_templa* $PWD
    echo "Created media, static, and templates directories."
    echo ""

    pip install -r requirements.txt
}


make_migrations_and_create_user()
{
  echo "Setting up migrations..."
  python3.6 manage.py migrate

  echo "Create a new superuser..."
  python3.6 manage.py createsuperuser
}

make_git_repo()
{
  echo "Initializing git..."
  git init
  git add *
  git commit -m "Initial commit"
}

run_server()
{
  PORT=3001
  echo "Running server on port $PORT"
  python3.6 manage.py runserver $PORT
}

copy_content()
{
    cp $CUR_DIR/Templated/_appfiles_/*.py $PWD
    echo "Copied application files."
    echo ""
}


# ----------------------------------------
# ----------------------------------------
# ----------------------------------------


make_app()
{
  echo "Inside $PWD"
  django-admin startapp $1

  mkdir -p _templates_/$1
  cd _templates_
  touch $1/home.html
  touch $1/create.html
  touch $1/edit.html
  touch $1/detail.html

  # Leaves _templates_
  cd ..

  # Enters application directory
  cd $1

  # Copies application files.
  copy_content $1

  # Leaves application directory
  cd ..
}



# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------
# ----------------------------------------



if [ "$SITE" ]; then
  if [ "$SITE" = "-h" ]; then
    print_help
  else
      make_main
      make_static

    # Creating apps and respective html files
    for i in $@; do
      if [ "$i" != "$SITE" ]; then
        echo "Creating application $i ..."
        make_app $i
      fi
    done

    make_migrations_and_create_user
    make_git_repo
    run_server

    # Leaves project directory
    cd ..

    # end of project creation...
    echo "Project: `$SITE` was created inside $PWD."

  fi
else
  print_usage
fi
