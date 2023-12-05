# System-project
My project was created in the system's class with the goal of identifying and comparing VCF files within a specified path. The code, when invoked by main.sh, will recursively explore the provided path. Subsequently, all files ending with the .vcf extension will be gathered and compared individually.

The primary options available for customizing the code to meet your requirements are as follows:

git ./main.sh /Path/to/data

This script locates all VCF files within the subdirectories of the provided path and calculates the number of variants between each pair of files.

Additional options can be appended after the path to enhance the script's functionality:

    -h: Display this help message
    -v: Display the script's version
    -g int: Modify the gap between variants (default = 0)
    -t int: Adjust the variant threshold (default = 0.75)


Provided with these scripts is a small utility script for automating the push of changes made to your main Git branch. You can utilize it in either of the following ways:

1. Directly execute the script with a commit message:

./autopush "Message for the commit"

2. Alternatively, you can simplify its usage by adding an alias to your bashrc file:

alias TheAliasNeeded='~/Desktop/Cours/auto_push.sh' >> ~/.bashrc

Then, you can use the alias along with your commit message:

TheAliasNeeded "The commit message"

This alias streamlines the process, making it more convenient for you to push changes automatically to your Git main branch.
