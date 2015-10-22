# teletask-dl
A small python script that downloads all podcasts of a given lecture from tele-task.de.

## Usage

    $ teletask-dl.py [URL] [MODE] [LOCATION]

    [URL]
        The URL of the overview page. (required)

    [MODE]
        -C    Create list of download links.
              Does not download anything.
              List is writen to stdout but you can pipe it anywhere.

        -D    Download every podcast.
              This may take some time and produce trafic.

        default: -C

    [LOCATION]
        The location to
         * the file where the list of links shall be stored (if MODE = -C)
         * the folder where to store the podcasts (if MODE = -D).

        If no LOCATION is given the link list will be written to stdout
        and podcasts will be stored in the current working directory.
