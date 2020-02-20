from directory_manager import DirectoryManager
from get_parameters import get_user_parameters
import sys


if __name__ == "__main__":
    print(sys.version)
    
    # get parameters from command line
    ftp_website, local_directory, max_depth, refresh_frequency, nb_multi, excluded_extensions = get_user_parameters()

    # init directory manager with local directory and maximal depth
    directory_manager = DirectoryManager(ftp_website, local_directory, max_depth, nb_multi, excluded_extensions)

    # launch the synchronization
    directory_manager.synchronize_directory(refresh_frequency)

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    # useless here because program loop never stops, but would be useful if included in a bigger project
    directory_manager.catchRemainingProcesses()
    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
