# encoding: utf-8
"""
Application dependencies related tasks for Invoke.
"""
import logging
import os
import shutil
import zipfile

from invoke import ctask as task

from tasks.utils import download_file


log = logging.getLogger(__name__) # pylint: disable=invalid-name


@task
def install_python_dependencies(context, force=False):
    """
    Install Python dependencies listed in requirements.txt.
    """
    log.info("Installing project dependencies...")
    context.run("pip install -r app/requirements.txt %s" % ('--upgrade' if force else ''))
    log.info("Project dependencies are installed.")

@task
def install_swagger_ui(context, force=False):
    # pylint: disable=unused-argument
    """
    Install Swagger UI HTML/JS/CSS assets.
    """
    log.info("Installing Swagger UI assets...")

    try:
        os.makedirs(os.path.join(context.app.static_root, 'bower'))
    except FileExistsError:
        pass

    swagger_ui_zip_filepath = os.path.join(context.app.static_root, 'bower', 'swagger-ui.zip')
    swagger_ui_root = os.path.join(context.app.static_root, 'bower', 'swagger-ui')

    if force:
        try:
            os.remove(swagger_ui_zip_filepath)
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(swagger_ui_root)
        except FileNotFoundError:
            pass

    # We are going to install Swagger UI from a fork which includes useful patches
    log.info("Downloading Swagger UI assets...")
    download_file(
        url="https://github.com/frol/swagger-ui/archive/master.zip",
        local_filepath=swagger_ui_zip_filepath
    )

    # Unzip swagger-ui.zip/dist into swagger-ui folder
    log.info("Unpacking Swagger UI assets...")
    with zipfile.ZipFile(swagger_ui_zip_filepath) as swagger_ui_zip_file:
        for zipped_member in swagger_ui_zip_file.infolist():
            zipped_member_path = os.path.relpath(zipped_member.filename, 'swagger-ui-master')

            # We only need the 'dist' folder
            if not os.path.commonpath([zipped_member_path, 'dist']):
                continue

            extract_path = os.path.join(swagger_ui_root, zipped_member_path)
            if not os.path.split(zipped_member.filename)[1]:
                # If the path is folder, just create a folder
                try:
                    os.makedirs(extract_path)
                except FileExistsError:
                    pass
            else:
                # Otherwise, read zipped file contents and write them to a file
                with swagger_ui_zip_file.open(zipped_member) as zipped_file:
                    with open(extract_path, mode='wb') as unzipped_file:
                        unzipped_file.write(zipped_file.read())

    log.info("Swagger UI is installed.")

@task
def install(context):
    # pylint: disable=unused-argument
    """
    Install project dependencies.
    """
    install_python_dependencies(context)
    install_swagger_ui(context)
