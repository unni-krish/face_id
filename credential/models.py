from django.db import models
import os

def rename_userphoto(instance, filename):
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Generate the new filename using the username and file extension
    new_filename = f"{instance.username}{ext}"
    # Define the destination path
    destination_path = os.path.join('userphoto', new_filename)

    # Check if a file with the same name already exists
    if os.path.exists(destination_path):
        # Remove the existing file
        os.remove(destination_path)

    # Return the path to store the file
    return destination_path


def rename_cv(instance, filename):
    # Get the file extension
    ext = os.path.splitext(filename)[1]
    # Generate the new filename using the username and file extension
    new_filename = f"{instance.username}{ext}"
    # Define the destination path
    destination_path = os.path.join('cv', new_filename)

    # Check if a file with the same name already exists
    if os.path.exists(destination_path):
        # Remove the existing file
        os.remove(destination_path)

    # Return the path to store the file
    return destination_path


class face_reg(models.Model):
    username = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    address = models.CharField(max_length=250)
    education = models.CharField(max_length=128)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=128)
    cpassword = models.CharField(max_length=128)
    userphoto = models.ImageField(upload_to=rename_userphoto)
    cv = models.ImageField(upload_to=rename_cv)

    def save(self, *args, **kwargs):
        # Check if the instance has a primary key (existing object)
        if self.pk is not None:
            # Retrieve the old instance
            old_instance = face_reg.objects.get(pk=self.pk)

            # Check if the userphoto field has changed
            if self.userphoto != old_instance.userphoto:
                # Remove the existing userphoto file
                if os.path.exists(old_instance.userphoto.path):
                    os.remove(old_instance.userphoto.path)

            # Check if the cv field has changed
            if self.cv != old_instance.cv:
                # Remove the existing cv file
                if os.path.exists(old_instance.cv.path):
                    os.remove(old_instance.cv.path)

        # Rename the userphoto and cv files before saving
        self.userphoto.name = rename_userphoto(self, self.userphoto.name)
        self.cv.name = rename_cv(self, self.cv.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
